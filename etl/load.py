import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus  # <-- Crucial import for encoding special characters

# Load environment variables from .env file
load_dotenv()

def get_db_engine():
    """
    Creates a SQLAlchemy database engine using credentials from the .env file.
    """
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    # URL-encode the password to safely handle special characters like '@'
    safe_password = quote_plus(db_password)
    
    # Construct the PostgreSQL connection string using the encoded password
    connection_string = f"postgresql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}"
    
    return create_engine(connection_string)

def create_tables_from_sql():
    """
    Executes the create_tables.sql file to initialize/recreate the database schema.
    This should be called before loading data to ensure tables exist.
    """
    print("🗄️  Creating/Recreating Database Tables...")
    
    try:
        engine = get_db_engine()
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'create_tables.sql')
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        with engine.connect() as connection:
            connection.execute(text(sql_script))
            connection.commit()
        
        print("✅ Database tables created successfully!\n")
        
    except Exception as e:
        print(f"❌ Critical Error during Table Creation: {e}")
        raise e

def load_data(transformed_datasets):
    """
    Loads transformed DataFrames into the PostgreSQL database.
    """
    print("🚀 Starting Load Phase...")
    
    try:
        engine = get_db_engine()
        
        # Define the exact order to append data to respect Foreign Key constraints
        load_order = [
            ('dim_dates', 'dim_dates'),
            ('dim_customers', 'dim_customers'),
            ('dim_sellers', 'dim_sellers'),
            ('dim_products', 'dim_products'),
            ('dim_payments', 'dim_payments'),
            ('fact_sales', 'fact_sales')
        ]
        
        for df_key, table_name in load_order:
            df = transformed_datasets[df_key]
            print(f" Loading {len(df)} rows into {table_name}...")
            
            df.to_sql(
                name=table_name, 
                con=engine, 
                if_exists='append', 
                index=False, 
                chunksize=10000
            )
            
        print("✅ Load Phase Complete. Data Warehouse fully populated!\n")
        
    except Exception as e:
        print(f"❌ Critical Error during Load Phase: {e}")
        raise e

if __name__ == "__main__":
    # Test connection block
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            print("🔗 Database connection test successful!")
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")