import sys
import os
import json

# Add 'src' directory to the module search path
sys.path.insert(0, os.path.abspath('src'))

try:
    from data_preparation import process_lender_offer_dataset 
    from train_model import train_and_save_model
    from evaluate_model import evaluate_model
except ImportError as e:
    raise ImportError(f"❌ Failed to import a module: {e}")

# Define data file path
data_file_path = 'data/raw/lender_offers.json'
output_file_path = 'data/processed/processed_lender_offers.csv'

# Check if the data file exists
if not os.path.exists(data_file_path):
    raise FileNotFoundError(f"❌ Data file not found: {data_file_path}")

# Load data
X_train, X_test, y_train, y_test = process_lender_offer_dataset(data_file_path, output_file_path)

# Train model
train_and_save_model(X_train, y_train, 'models/random_forest_model.pkl')

# Evaluate
metrics = evaluate_model('models/random_forest_model.pkl', X_test, y_test)

# Save metrics
metrics_file_path = 'models/metrics.json'
os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)
with open(metrics_file_path, 'w') as f:
    json.dump(metrics, f, indent=4)

print(f"✅ Metrics saved to {metrics_file_path}")