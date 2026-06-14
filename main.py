import sys
import time
from etl.extract import extract_raw_data
from etl.transform import transform_data
from etl.load import load_data

def run_pipeline():
    """
    Main execution engine that orchestrates the Extract, Transform, 
    and Load phases sequentially.
    """
    start_time = time.time()
    print("=============================================")
    print("🏁 STARTING E-COMMERCE DATA WAREHOUSE PIPELINE 🏁")
    print("=============================================\n")
    
    try:
        # 1. EXTRACT
        raw_datasets = extract_raw_data()
        
        # 2. TRANSFORM
        transformed_tables = transform_data(raw_datasets)
        
        # 3. LOAD
        load_data(transformed_tables)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        print("=============================================")
        print(f"🎉 SUCCESS: Pipeline completed execution cleanly!")
        print(f"⏱️ Total Time Elapsed: {duration} seconds")
        print("=============================================")

    except Exception as e:
        print("\n❌ PIPELINE EXECUTION FAILED ❌")
        print(f"Error Context: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()