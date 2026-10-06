# -*- coding: utf-8 -*-
"""soil_prototype_pipeline_v1_0.ipynb
"""

# Cell 1: Environment Setup & Authentication
from google.colab import drive
import ee

# 1. Mount your Google Drive
# (This will pop up a window asking for permission to access your Drive)
drive.mount('/content/drive')

# 2. Install the Gaussian Process library
!pip install gpflow -q

# 3. Authenticate and Initialize Earth Engine
# (This will generate a link. Click it, log in, and copy the authorization code it gives you back into the prompt box here)
ee.Authenticate()

# Replace 'YOUR-PROJECT-ID' with the Project ID you created in Step 1
ee.Initialize(project= '')

print("Environment Successfully Initialized!")

import os
# This will force the runtime to restart.
# After the restart, you can run the subsequent cells without the numpy error.
os._exit(00)

import numpy as np
import pandas as pd
import gpflow
import tensorflow as tf

print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"GPflow version: {gpflow.__version__}")
print(f"TensorFlow version: {tf.__version__}")

# Cell 3: Earth Engine Sensor Pointers (Targeted ROI)
import ee
import pandas as pd

# Ensure Earth Engine is initialized for the specific project
try:
    ee.Initialize(project='')
except Exception:
    ee.Authenticate()
    ee.Initialize(project='')

# Define the targeted UNL Research Meadow ROI
# Centered at 42.13 N, -99.38 W with a tight bounding box
roi = ee.Geometry.Polygon([
])

# 1. SRTM Topography (Geomorphic Chips - 30m resolution)
dem = ee.Image('USGS/SRTMGL1_003')
terrain = ee.Terrain.products(dem)

# 2. Sentinel-2 (Aboveground Biomass / SAVI)
def add_savi(image):
    savi = image.expression(
        '((NIR - RED) / (NIR + RED + 0.5)) * (1.5)', {
            'NIR': image.select('B8'),
            'RED': image.select('B4')
        }).rename('SAVI')
    return image.addBands(savi)

s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(roi) \
    .map(add_savi)

# 3. Sentinel-1 (Surface Roughness / Moisture Proxy)
s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
    .filterBounds(roi) \
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
    .select('VV')

print("Sensor Pointers Successfully Locked to UNL Meadow ROI.")

# Cell 4: Automated Real Covariate Extraction
import pandas as pd
import ee

print("Extracting Earth Engine covariates for real field data...")

# Load your real data from Drive - Updated path with correct hyphens
data_path = '/content/drive/My Drive/Sandhills_Carbon_Prototype/data/empirical/sandhills-empirical-fractions.csv'
df_real = pd.read_csv(data_path)

# Create empty columns for the new environmental data
df_real['Elevation'] = 0.0
df_real['Slope'] = 0.0
df_real['SAVI_8yr_Mean'] = 0.0

# Extract data for each unique pasture centroid
unique_pastures = df_real[['Treatment', 'Lat', 'Lon']].drop_duplicates()

for index, row in unique_pastures.iterrows():
    # Ping Earth Engine
    point = ee.Geometry.Point([row['Lon'], row['Lat']])

    # Get Topography
    terrain_data = terrain.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=30).getInfo()

    # Get 8-year median SAVI (2010 to 2018)
    s2_median = s2_collection.filterDate('2010-04-01', '2018-04-30').median()
    savi_data = s2_median.select('SAVI').reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=10).getInfo()

    # Map the extracted values back to ALL replicates of this treatment
    mask = df_real['Treatment'] == row['Treatment']
    if terrain_data and 'elevation' in terrain_data:
        df_real.loc[mask, 'Elevation'] = terrain_data['elevation']
        df_real.loc[mask, 'Slope'] = terrain_data['slope']
    if savi_data and 'SAVI' in savi_data:
        df_real.loc[mask, 'SAVI_8yr_Mean'] = savi_data['SAVI']

print("Extraction Complete! Your dataframe is now populated with real spatial metrics.")
display(df_real.head())

# Cell 5: High-Fidelity GPR Engine
import gpflow
import tensorflow as tf
import numpy as np

print("Re-training with High-Fidelity Lengthscales...")

# 1. Calculate the Delta using Total Carbon (MAOM + OPOM + FPOM)
df_real['Total_C_2010'] = df_real['MAOM_2010'] + df_real['OPOM_2010'] + df_real['FPOM_2010']
df_real['Total_C_2018'] = df_real['MAOM_2018'] + df_real['OPOM_2018'] + df_real['FPOM_2018']
df_real['Delta_Total']  = df_real['Total_C_2018'] - df_real['Total_C_2010']

# 2. Setup Tensors
X_features = ['Total_C_2010', 'Stocking_Density', 'Slope', 'SAVI_8yr_Mean']
X_data = df_real[X_features].values
Y_data = df_real[['Delta_Total']].values

X_train_tf = tf.convert_to_tensor(X_data, dtype=tf.float64)
Y_train_tf = tf.convert_to_tensor(Y_data, dtype=tf.float64)

# 3. Print feature standard deviations so you can see what the optimizer is working with
print("Feature std devs (use as lengthscale ballpark):")
for feat, std in zip(X_features, X_data.std(axis=0)):
    print(f"  {feat}: {std:.2f}")

# 4. ARD Matern52 Kernel
# Lengthscales initialized ~1x the std of each feature:
#   Total_C_2010     ~5.0   (C range ~15-25 g/kg)
#   Stocking_Density ~75000 (range 0 to 214138 kg/ha)
#   Slope            ~2.0   (gentle meadow terrain)
#   SAVI_8yr_Mean    ~0.15  (NDVI-like index 0-1)
kernel = gpflow.kernels.Matern52(
    lengthscales=[5.0, 75000.0, 2.0, 0.15],
    active_dims=[0, 1, 2, 3]
)

# 5. Constant Mean Function
mean_fn = gpflow.mean_functions.Constant(c=np.array([0.0]))

model = gpflow.models.GPR(
    data=(X_train_tf, Y_train_tf),
    kernel=kernel,
    mean_function=mean_fn
)

# 6. Optimize
opt = gpflow.optimizers.Scipy()
opt.minimize(model.training_loss, model.trainable_variables)

# Print optimized lengthscales so you can verify the optimizer moved them
print("\nOptimized lengthscales:")
for feat, ls in zip(X_features, model.kernel.lengthscales.numpy()):
    print(f"  {feat}: {ls:.2f}")

print("\nOptimization Complete.")

# Cell 6: Universal 10-Year and 20-Year ML Projection Loop
import pandas as pd
import numpy as np

print("Running Dual-Timeline Carbon Projections for All Treatments...")

# Residual floor: soils never reach zero SOM — 2.0 g/kg is a conservative minimum
RESIDUAL_FLOOR = 2.0

all_projections = []
treatments = df_real['Treatment'].unique()

for treat in treatments:
    subset = df_real[df_real['Treatment'] == treat]

    # --- FIX: use 2010 baseline as model input (matches training features) ---
    baseline_c = subset['Total_C_2010'].mean()   # model was trained on this
    current_c  = subset['Total_C_2018'].mean()   # projection anchors from here forward

    density   = subset['Stocking_Density'].iloc[0]
    avg_slope = subset['Slope'].mean()
    avg_savi  = subset['SAVI_8yr_Mean'].mean()

    # GPR input must match Cell 5 X_features order:
    # [Total_C_2010, Stocking_Density, Slope, SAVI_8yr_Mean]
    X_input = np.array([[baseline_c, density, avg_slope, avg_savi]])

    mean_delta, var_delta = model.predict_f(X_input)

    # Annual rate derived from the 8-year predicted delta
    annual_rate = mean_delta.numpy()[0][0] / 8.0

    # Project forward from the 2018 anchor, not from 2010
    projected_2028 = max(RESIDUAL_FLOOR, current_c + (annual_rate * 10))
    projected_2038 = max(RESIDUAL_FLOOR, current_c + (annual_rate * 20))

    uncertainty = np.sqrt(var_delta.numpy()[0][0])

    all_projections.append({
        'Treatment':          treat,
        '2018_Baseline':      round(current_c, 3),
        '2028_Projected':     round(projected_2028, 3),
        '2038_Projected':     round(projected_2038, 3),
        'Net_20yr_Change':    round(projected_2038 - current_c, 3),
        'Annual_Accrual':     round(annual_rate, 4),
        'Model_Confidence_σ': round(uncertainty, 4)
    })

projection_summary = pd.DataFrame(all_projections)

print("\n--- Dual-Timeline Management Forecast ---")
display(projection_summary)

# Cell 7: Uncertainty Extraction (Shadow Map)
print("Extracting Shadow Map Variance...")

# Build a realistic grid spanning the actual feature ranges seen in training data
# [Total_C_2010, Stocking_Density, Slope, SAVI_8yr_Mean]
n_points = 100
np.random.seed(42)

spatial_grid = np.column_stack([
    np.random.uniform(14.0, 22.0, n_points),    # Total_C_2010: realistic 0-10cm range
    np.full(n_points, 7138.0),                   # Hold density fixed at 4PR1 level
    np.random.uniform(0.5, 4.0,  n_points),      # Slope: gentle Sandhills meadow terrain
    np.random.uniform(0.25, 0.65, n_points),     # SAVI_8yr_Mean: realistic vegetation index
])

mean_predictions, variances = model.predict_f(spatial_grid)

uncertainty_array = variances.numpy().flatten()
top_3_uncertain   = np.argsort(uncertainty_array)[-3:]

print("\n--- ACTIVE LEARNING PROTOCOL ---")
print(f"Uncertainty range across grid: {uncertainty_array.min():.3f} – {uncertainty_array.max():.3f}")
print("Highest uncertainty at grid indices:", top_3_uncertain)
print("C baseline values at those points:",
      [round(spatial_grid[i, 0], 2) for i in top_3_uncertain])
print("Recommendation: Target these C-stock zones for next physical soil probe sampling.")

# Cell 8: Hybrid Professional MRV Dashboard (ML + Fractional)
# ⚠️  Requires projection_summary (Cell 6) and results_df (Cell 9) — run those first
import folium
from folium import plugins
import branca
import numpy as np
import pandas as pd

try:
    print("Finalizing Hybrid Interactive Dashboard...")

    map_data = projection_summary.copy()
    coords   = df_real.groupby('Treatment')[['Lat', 'Lon', 'Stocking_Density']].mean().reset_index()
    map_data = map_data.merge(coords, on='Treatment')

    # --- FIX: colormap range updated to reflect corrected GPR output ---
    # 4PR1 now projects positive; CNT projects negative
    net_min = map_data['Net_20yr_Change'].min()
    net_max = map_data['Net_20yr_Change'].max()
    colormap = branca.colormap.LinearColormap(
        colors=['#e53e3e', '#fbd38d', '#48bb78'],
        index=[net_min, 0, net_max],
        vmin=net_min, vmax=net_max,
        caption='GPR Projected 20-yr Net Change (g C kg⁻¹)'
    )

    m = folium.Map(
        location=[map_data['Lat'].mean(), map_data['Lon'].mean()],
        zoom_start=15,
        tiles=None
    )

    folium.TileLayer(tiles='CartoDB dark_matter',   name='Dark Mode Base',   control=False).add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                     attr='Google Satellite', name='Satellite Imagery', overlay=False, control=True).add_to(m)

    group_2028 = folium.FeatureGroup(name="10-Year Milestone (2028)", show=False)
    group_2038 = folium.FeatureGroup(name="20-Year Projection (2038)", show=True)

    for _, row in map_data.iterrows():
        treat        = row['Treatment']
        marker_color = colormap(row['Net_20yr_Change'])
        sat_pct      = min(100, (row['2038_Projected'] / 35.0) * 100)

        frac_subset = results_df[results_df['Treatment'] == treat]
        frac_rows   = ""
        for _, f_row in frac_subset.iterrows():
            frac_rows += f"""
            <tr style="border-bottom: 1px solid #edf2f7;">
                <td style="padding:2px;">{f_row['Fraction']}</td>
                <td style="text-align:right;">{f_row['Baseline_2018']:.2f}</td>
                <td style="text-align:right; font-weight:bold;">{f_row['Projected_2038']:.2f}</td>
            </tr>
            """

        html_content = f"""
        <div style="font-family: Arial; width: 280px; padding: 5px;">
            <h4 style="margin:0; color:{marker_color};">{treat} Management</h4>
            <p style="font-size:10px; color:#718096; margin:0;">Density: {row['Stocking_Density']:,.0f} kg/ha</p>
            <div style="background:#f7fafc; padding:8px; border-radius:5px; margin-top:10px; border-left:4px solid {marker_color};">
                <p style="font-size:11px; margin:0; color:#2d3748;"><b>GPR System Prediction (ML)</b></p>
                <table style="width:100%; font-size:11px; color:#2d3748;">
                    <tr><td>2038 Projected:</td><td style="text-align:right;"><b>{row['2038_Projected']:.2f} g/kg</b></td></tr>
                    <tr><td>Net 20-yr Change:</td><td style="text-align:right;">{row['Net_20yr_Change']:+.2f} g/kg</td></tr>
                    <tr><td>Confidence (σ):</td><td style="text-align:right;">±{row['Model_Confidence_σ']:.2f}</td></tr>
                </table>
            </div>
            <p style="font-size:11px; margin:10px 0 4px 0; color:#2d3748;"><b>Linear Fractional Potential</b></p>
            <table style="width:100%; font-size:10px; border-collapse:collapse; color:#4a5568;">
                <tr style="color:#718096; border-bottom:1px solid #cbd5e0;">
                    <th style="text-align:left;">Fraction</th>
                    <th style="text-align:right;">2018</th>
                    <th style="text-align:right;">2038</th>
                </tr>
                {frac_rows}
            </table>
            <div style="width:100%; background:#edf2f7; height:6px; margin-top:12px; border-radius:3px;">
                <div style="width:{sat_pct:.1f}%; background:{marker_color}; height:100%; border-radius:3px;"></div>
            </div>
            <p style="font-size:9px; color:#a0aec0; margin-top:4px; text-align:center;">Mineral saturation potential (35 g/kg ceiling)</p>
        </div>
        """

        folium.Circle(location=[row['Lat'], row['Lon']], radius=140,
                      color=marker_color, fill=True, fill_opacity=0.3,
                      tooltip=f"{treat} 2028 Milestone").add_to(group_2028)

        folium.Circle(location=[row['Lat'], row['Lon']], radius=180,
                      color=marker_color, fill=True, fill_opacity=0.6,
                      popup=folium.Popup(html_content, max_width=350),
                      tooltip=f"<b>{treat}</b>: Click for Hybrid ML/Fractional Results").add_to(group_2038)

    group_2028.add_to(m)
    group_2038.add_to(m)
    m.add_child(colormap)
    plugins.Fullscreen().add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    title_html = '''<h3 align="center" style="font-size:16px; font-family:Arial; color:white;
        position: fixed; top: 10px; left: 50px; z-index:9999;
        background: rgba(0,0,0,0.5); padding: 8px; border-radius: 5px;">
        <b>Hybrid MRV Forecast: ML System vs. Fractional Potential</b></h3>'''
    m.get_root().html.add_child(folium.Element(title_html))

    display(m)

except NameError as e:
    print(f"ERROR: Missing required dataframes. {e}")
    print("Run order must be: Cell 5 → Cell 6 → Cell 9 → Cell 8")

# Cell 9: Fractional Linear Projections
# ⚠️  Run this cell BEFORE Cell 8 (dashboard) — it creates results_df
import pandas as pd
import numpy as np

print("Compiling fractional projection results...")

fractions     = ['MAOM', 'OPOM', 'FPOM', 'DOM']
export_rows   = []
RESIDUAL_FLOOR = 1.0  # g/kg — minimum physically plausible fraction value

# --- FIX: use .mean() so all replicates contribute, not just the first row ---
pasture_summary = df_real.groupby('Treatment').mean(numeric_only=True).reset_index()

for _, row in pasture_summary.iterrows():
    treatment = row['Treatment']

    for f in fractions:
        c_2010 = row[f'{f}_2010']
        c_2018 = row[f'{f}_2018']

        annual_rate = (c_2018 - c_2010) / 8.0

        # --- FIX: floor at RESIDUAL_FLOOR instead of 0.0 ---
        proj_2028 = max(RESIDUAL_FLOOR, c_2018 + (annual_rate * 10))
        proj_2038 = max(RESIDUAL_FLOOR, c_2018 + (annual_rate * 20))

        export_rows.append({
            'Treatment':       treatment,
            'Fraction':        f,
            'Baseline_2010':   round(c_2010, 4),
            'Baseline_2018':   round(c_2018, 4),
            'Projected_2028':  round(proj_2028, 4),
            'Projected_2038':  round(proj_2038, 4),
            'Annual_Rate_g_kg': round(annual_rate, 4),
            'Net_20yr_Delta':  round(proj_2038 - c_2018, 4)
        })

results_df = pd.DataFrame(export_rows)

# Sanity check: print fraction sums so you can verify they match the GPR summary order of magnitude
print("\nFraction sums by treatment (2038):")
check = results_df.groupby('Treatment')['Projected_2038'].sum().reset_index()
check.columns = ['Treatment', 'Frac_Sum_2038']
display(check)

export_path = '/content/drive/My Drive/Sandhills_Carbon_Prototype/data/sandhills_20yr_projections.csv'
results_df.to_csv(export_path, index=False)
print(f"\nExported to: {export_path}")
display(results_df)

import os
import pickle
import gpflow

# 1. Define the Export Directory
export_path = '/content/drive/My Drive/Sandhills_Carbon_Prototype/outputs/Final_Results'
os.makedirs(export_path, exist_ok=True)

print(f"Exporting files to: {export_path}...")

# 2. Export the Tabular Data (CSV)
# This includes the linear fractional projections
results_df.to_csv(f'{export_path}/fractional_projections_2038.csv', index=False)

# This includes the GPR Machine Learning summary
projection_summary.to_csv(f'{export_path}/ml_projection_summary_2038.csv', index=False)

# 3. Export the Interactive Dashboard (HTML)
# This preserves all colors, layers, and hover effects for browser viewing
m.save(f'{export_path}/interactive_mrv_dashboard.html')

# 4. Export the Trained GPR Model (Pickle)
# This allows you to reload the model later without retraining
with open(f'{export_path}/gpr_carbon_model.pkl', 'wb') as f:
    pickle.dump(gpflow.utilities.parameter_dict(model), f)

print("✅ Export Complete! All data and the interactive map are now in your Drive.")