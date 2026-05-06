import os
import json
import pandas as pd
from git.repo.base import Repo
import mysql.connector
from sqlalchemy import create_engine
from pathlib import Path
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def clone_repo():
    """Clones the PhonePe Pulse repository if it doesn't exist."""
    repo_url = "https://github.com/PhonePe/pulse"
    clone_dir = Path("pulse")
    
    if not clone_dir.exists():
        try:
            print("Cloning PhonePe Pulse repository...")
            Repo.clone_from(repo_url, clone_dir)
            print("Repository cloned successfully.")
        except Exception as e:
            print(f"Error cloning repository: {e}")
    else:
        print("Repository already cloned.")

def extract_aggregated_transaction(base_path):
    """Extracts aggregated transaction data from JSON files."""
    data = []
    path = base_path / "data" / "aggregated" / "transaction" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['transactionData']:
                                for item in json_data['data']['transactionData']:
                                    name = item['name']
                                    count = item['paymentInstruments'][0]['count']
                                    amount = item['paymentInstruments'][0]['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'transaction_type': name,
                                        'transaction_count': count,
                                        'transaction_amount': amount
                                    })
    return pd.DataFrame(data)

def extract_aggregated_user(base_path):
    """Extracts aggregated user data from JSON files."""
    data = []
    path = base_path / "data" / "aggregated" / "user" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['usersByDevice']:
                                for item in json_data['data']['usersByDevice']:
                                    brand = item['brand']
                                    count = item['count']
                                    percentage = item['percentage']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'brand': brand,
                                        'user_count': count,
                                        'user_percentage': percentage
                                    })
    return pd.DataFrame(data)

def extract_aggregated_insurance(base_path):
    """Extracts aggregated insurance data from JSON files."""
    data = []
    path = base_path / "data" / "aggregated" / "insurance" / "country" / "india" / "state"
    if not path.exists():
        return pd.DataFrame(columns=['State', 'Year', 'Quarter', 'insurance_type', 'insurance_count', 'insurance_amount'])
        
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['transactionData']:
                                for item in json_data['data']['transactionData']:
                                    name = item['name']
                                    count = item['paymentInstruments'][0]['count']
                                    amount = item['paymentInstruments'][0]['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'insurance_type': name,
                                        'insurance_count': count,
                                        'insurance_amount': amount
                                    })
    return pd.DataFrame(data)

def extract_map_transaction(base_path):
    """Extracts map transaction data from JSON files."""
    data = []
    path = base_path / "data" / "map" / "transaction" / "hover" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['hoverDataList']:
                                for item in json_data['data']['hoverDataList']:
                                    district = item['name']
                                    count = item['metric'][0]['count']
                                    amount = item['metric'][0]['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'district': district,
                                        'transaction_count': count,
                                        'transaction_amount': amount
                                    })
    return pd.DataFrame(data)

def extract_map_user(base_path):
    """Extracts map user data from JSON files."""
    data = []
    path = base_path / "data" / "map" / "user" / "hover" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['hoverData']:
                                for district, details in json_data['data']['hoverData'].items():
                                    registered = details['registeredUsers']
                                    appOpens = details['appOpens']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'district': district,
                                        'registered_users': registered,
                                        'app_opens': appOpens
                                    })
    return pd.DataFrame(data)

def extract_map_insurance(base_path):
    """Extracts map insurance data from JSON files."""
    data = []
    path = base_path / "data" / "map" / "insurance" / "hover" / "country" / "india" / "state"
    if not path.exists():
        return pd.DataFrame(columns=['State', 'Year', 'Quarter', 'district', 'insurance_count', 'insurance_amount'])
        
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            if json_data['data']['hoverDataList']:
                                for item in json_data['data']['hoverDataList']:
                                    district = item['name']
                                    count = item['metric'][0]['count']
                                    amount = item['metric'][0]['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'district': district,
                                        'insurance_count': count,
                                        'insurance_amount': amount
                                    })
    return pd.DataFrame(data)

def extract_top_transaction(base_path):
    """Extracts top transaction data from JSON files."""
    data = []
    path = base_path / "data" / "top" / "transaction" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            
                            # Districts
                            if json_data['data']['districts']:
                                for item in json_data['data']['districts']:
                                    name = item.get('entityName', item.get('name'))
                                    metric = item['metric'] if isinstance(item['metric'], dict) else item['metric'][0]
                                    count = metric['count']
                                    amount = metric['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'district',
                                        'entity_name': name,
                                        'transaction_count': count,
                                        'transaction_amount': amount
                                    })
                            
                            # Pincodes
                            if json_data['data']['pincodes']:
                                for item in json_data['data']['pincodes']:
                                    name = item.get('entityName', item.get('name'))
                                    metric = item['metric'] if isinstance(item['metric'], dict) else item['metric'][0]
                                    count = metric['count']
                                    amount = metric['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'pincode',
                                        'entity_name': name,
                                        'transaction_count': count,
                                        'transaction_amount': amount
                                    })
    return pd.DataFrame(data)

def extract_top_user(base_path):
    """Extracts top user data from JSON files."""
    data = []
    path = base_path / "data" / "top" / "user" / "country" / "india" / "state"
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            
                            # Districts
                            if json_data['data']['districts']:
                                for item in json_data['data']['districts']:
                                    name = item.get('entityName', item.get('name'))
                                    registered = item['registeredUsers']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'district',
                                        'entity_name': name,
                                        'registered_users': registered
                                    })
                            
                            # Pincodes
                            if json_data['data']['pincodes']:
                                for item in json_data['data']['pincodes']:
                                    name = item.get('entityName', item.get('name'))
                                    registered = item['registeredUsers']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'pincode',
                                        'entity_name': name,
                                        'registered_users': registered
                                    })
    return pd.DataFrame(data)

def extract_top_insurance(base_path):
    """Extracts top insurance data from JSON files."""
    data = []
    path = base_path / "data" / "top" / "insurance" / "country" / "india" / "state"
    if not path.exists():
        return pd.DataFrame(columns=['State', 'Year', 'Quarter', 'entity_type', 'entity_name', 'insurance_count', 'insurance_amount'])
        
    for state in path.iterdir():
        if state.is_dir():
            for year in state.iterdir():
                if year.is_dir():
                    for file in year.glob("*.json"):
                        with open(file, 'r') as f:
                            json_data = json.load(f)
                            quarter = int(file.stem)
                            
                            # Districts
                            if json_data['data']['districts']:
                                for item in json_data['data']['districts']:
                                    name = item.get('entityName', item.get('name'))
                                    metric = item['metric'] if isinstance(item['metric'], dict) else item['metric'][0]
                                    count = metric['count']
                                    amount = metric['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'district',
                                        'entity_name': name,
                                        'insurance_count': count,
                                        'insurance_amount': amount
                                    })
                            
                            # Pincodes
                            if json_data['data']['pincodes']:
                                for item in json_data['data']['pincodes']:
                                    name = item.get('entityName', item.get('name'))
                                    metric = item['metric'] if isinstance(item['metric'], dict) else item['metric'][0]
                                    count = metric['count']
                                    amount = metric['amount']
                                    data.append({
                                        'State': state.name,
                                        'Year': int(year.name),
                                        'Quarter': quarter,
                                        'entity_type': 'pincode',
                                        'entity_name': name,
                                        'insurance_count': count,
                                        'insurance_amount': amount
                                    })
    return pd.DataFrame(data)

def create_database():
    """Creates the database and executes DDL schema."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Read and execute SQL schema
        schema_path = Path('sql_schema.sql')
        if schema_path.exists():
            with open(schema_path, 'r') as file:
                sql_script = file.read()
                
            # Split commands by semicolon to execute individually
            commands = sql_script.split(';')
            for command in commands:
                try:
                    if command.strip():
                        cursor.execute(command)
                except Exception as e:
                    print(f"Error executing SQL command: {e}")
            conn.commit()
            print("Database and tables created successfully.")
        else:
            print("Error: sql_schema.sql not found.")
            
    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def load_data_to_mysql(df, table_name):
    """Loads a DataFrame into a MySQL table."""
    if df.empty:
        print(f"Warning: DataFrame for {table_name} is empty. Skipping load.")
        return
        
    try:
        # Create connection string using SQLAlchemy
        db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        engine = create_engine(db_url)
        
        # Clean state names (replace hyphens with spaces and title case)
        if 'State' in df.columns:
            df['State'] = df['State'].str.replace('-', ' ').str.title()
            
        print(f"Loading {len(df)} rows into {table_name}...")
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f"Data loaded successfully into {table_name}.")
    except Exception as e:
        print(f"Error loading data to {table_name}: {e}")

def main():
    print("Starting data extraction pipeline...")
    
    # 1. Clone repository
    clone_repo()
    
    # 2. Extract data into DataFrames
    base_path = Path("pulse")
    if not base_path.exists():
        print("Error: pulse repository not found. Check cloning step.")
        return
        
    print("\nExtracting data from JSON files...")
    df_agg_trans = extract_aggregated_transaction(base_path)
    df_agg_user = extract_aggregated_user(base_path)
    df_agg_ins = extract_aggregated_insurance(base_path)
    
    df_map_trans = extract_map_transaction(base_path)
    df_map_user = extract_map_user(base_path)
    df_map_ins = extract_map_insurance(base_path)
    
    df_top_trans = extract_top_transaction(base_path)
    df_top_user = extract_top_user(base_path)
    df_top_ins = extract_top_insurance(base_path)
    
    # 3. Create Database and Schema
    print("\nSetting up database...")
    create_database()
    
    # 4. Load Data into MySQL
    print("\nLoading data into MySQL database...")
    load_data_to_mysql(df_agg_trans, 'Aggregated_transaction')
    load_data_to_mysql(df_agg_user, 'Aggregated_user')
    load_data_to_mysql(df_agg_ins, 'Aggregated_insurance')
    
    load_data_to_mysql(df_map_trans, 'Map_transaction')
    load_data_to_mysql(df_map_user, 'Map_user')
    load_data_to_mysql(df_map_ins, 'Map_insurance')
    
    load_data_to_mysql(df_top_trans, 'Top_transaction')
    load_data_to_mysql(df_top_user, 'Top_user')
    load_data_to_mysql(df_top_ins, 'Top_insurance')
    
    print("\nData extraction and loading completed successfully!")

if __name__ == "__main__":
    main()
