import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Paths
csv_path = os.path.join('backend', 'static', 'csvfile')
models_dir = os.path.join('backend', 'static', 'models')

# Read CSV (csvfile is a file, not a directory)
df = pd.read_csv(csv_path)

# Encode 'season' as integer
season_le = LabelEncoder()
df['season_encoded'] = season_le.fit_transform(df['season'])

# Save the label encoder for later use if needed
le_path = os.path.join('backend', 'static', 'labelencoder', 'season_le.joblib')
dump(season_le, le_path)

# Features to use
feature_cols = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall', 'area', 'season_encoded']
target_col = 'production'

# Train a model for each crop
df['crop'] = df['crop'].str.lower()
crops = df['crop'].unique()

for crop in crops:
    crop_df = df[df['crop'] == crop]
    X = crop_df[feature_cols]
    y = crop_df[target_col]
    if len(crop_df) < 5:
        print(f"Skipping {crop}: not enough data.")
        continue
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    model_path = os.path.join(models_dir, f"{crop}.joblib")
    dump(model, model_path)
    print(f"Trained and saved model for {crop} -> {model_path}")

print("All models trained and saved.")
