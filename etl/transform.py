import pandas as pd

def transform_data(datasets):
    """
    Takes the dictionary of raw DataFrames and transforms them 
    into a structured Star Schema format.
    """
    print("⚙️ Starting Transformation Phase...")
    
    # Extract raw dataframes from the incoming dictionary
    orders = datasets['orders'].copy()
    items = datasets['order_items'].copy()
    customers = datasets['customers'].copy()
    products = datasets['products'].copy()
    translations = datasets['translations'].copy()
    payments = datasets['payments'].copy()
    sellers = datasets['sellers'].copy()

    # --- 1. DIM_DATES ---
    print(" Building dim_dates...")
    # Convert string to datetime objects
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    
    # Drop duplicates to unique dates for our dimension table
    date_series = orders['order_purchase_timestamp'].dt.normalize().unique()
    dim_dates = pd.DataFrame({'date_key': date_series})
    
    # Extract temporal attributes
    dim_dates['year'] = dim_dates['date_key'].dt.year
    dim_dates['month'] = dim_dates['date_key'].dt.month
    dim_dates['day'] = dim_dates['date_key'].dt.day
    dim_dates['day_of_week'] = dim_dates['date_key'].dt.day_name()
    dim_dates['quarter'] = dim_dates['date_key'].dt.quarter

    # --- 2. DIM_PRODUCTS ---
    print(" Building dim_products...")
    # Merge with translations to get English names
    dim_products = pd.merge(products, translations, on='product_category_name', how='left')
    # Drop the original Portuguese column and rename the English column
    dim_products = dim_products.drop(columns=['product_category_name'])
    dim_products = dim_products.rename(columns={'product_category_name_english': 'product_category'})
    # Fill missing categories with 'unknown'
    dim_products['product_category'] = dim_products['product_category'].fillna('unknown')

    # --- 3. FACT_SALES ---
    print(" Building fact_sales...")
    # Convert remaining timestamp columns in orders for integrity
    timestamp_cols = ['order_approved_at', 'order_delivered_carrier_date', 
                      'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in timestamp_cols:
        orders[col] = pd.to_datetime(orders[col])
        
    # Merge items with parent orders to construct the fact table
    fact_sales = pd.merge(items, orders, on='order_id', how='inner')
    
    # Create an explicit date link back to dim_dates
    fact_sales['date_key'] = fact_sales['order_purchase_timestamp'].dt.normalize()
    
    # Select and order final columns for our warehouse
    fact_sales = fact_sales[[
        'order_id', 
        'order_item_id',
        'customer_id', 
        'product_id', 
        'seller_id', 
        'date_key',
        'price', 
        'freight_value', 
        'order_status', 
        'order_delivered_customer_date'
    ]]

    # --- 4. DIM_CUSTOMERS, DIM_SELLERS, DIM_PAYMENTS ---
    # These map closely to their raw counterparts, renamed for schema clarity
    print(" Formatting remaining dimensions...")
    dim_customers = customers.rename(columns={'customer_zip_code_prefix': 'zip_code'})
    dim_sellers = sellers.rename(columns={'seller_zip_code_prefix': 'zip_code'})
    dim_payments = payments.copy()

    print("✅ Transformation Phase Complete.\n")
    
    # Return everything neatly packaged
    return {
        'fact_sales': fact_sales,
        'dim_customers': dim_customers,
        'dim_products': dim_products,
        'dim_sellers': dim_sellers,
        'dim_payments': dim_payments,
        'dim_dates': dim_dates
    }

if __name__ == "__main__":
    # Test execution block by linking Extract -> Transform directly
    from extract import extract_raw_data
    try:
        raw_data = extract_raw_data()
        transformed_data = transform_data(raw_data)
        print(f"Fact Table Rows: {len(transformed_data['fact_sales'])}")
        print("Transformation test passed successfully!")
    except Exception as e:
        print(f"❌ Transformation test failed: {e}")