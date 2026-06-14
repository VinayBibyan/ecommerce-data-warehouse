import os
import pandas as pd

def extract_raw_data(data_dir='data/raw'):
    """
    Reads raw CSV files from the specified directory.
    Returns a dictionary of Pandas DataFrames.
    """
    print("🚀 Starting Extraction Phase...")
    
    # Dictionary to hold our DataFrames
    datasets = {}
    
    # List of files we need for our Star Schema
    files_to_load = {
        'orders': 'orders_dataset.csv',
        'order_items': 'order_items_dataset.csv',
        'customers': 'customers_dataset.csv',
        'products': 'products_dataset.csv',
        'translations': 'product_category_name_translation.csv',
        'payments': 'order_payments_dataset.csv',
        'sellers': 'sellers_dataset.csv'
    }
    
    for key, file_name in files_to_load.items():
        file_path = os.path.join(data_dir, file_name)
        
        if os.path.exists(file_path):
            print(f" Reading {file_name}...")
            datasets[key] = pd.read_csv(file_path)
        else:
            raise FileNotFoundError(f"❌ Critical file missing: {file_path}")
            
    print("✅ Extraction Phase Complete. All data loaded into memory.\n")
    return datasets

# Quick manual test block
if __name__ == "__main__":
    # If running this file directly, check if it works from the project root
    # Adjust path if running directly inside the etl folder
    try:
        data = extract_raw_data()
        print(f"Successfully loaded {len(data)} datasets.")
    except Exception as e:
        print(f"Extraction test failed: {e}")