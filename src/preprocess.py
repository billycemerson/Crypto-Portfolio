import pandas as pd
import os

def preprocess_crypto_data(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate through all CSV files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, file_name)
            
            print(f"Processing {file_name}...")
            
            try:
                # Read the raw data
                data = pd.read_csv(input_file)
                
                # Parse the 'Date' column as datetime
                data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
                
                # Convert numeric columns to proper types
                cols_to_convert = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
                data[cols_to_convert] = data[cols_to_convert].apply(pd.to_numeric, errors='coerce')
                
                # Drop the first row (metadata or invalid data)
                data = data.iloc[1:].reset_index(drop=True)
                
                # Drop rows with invalid or missing 'Date'
                data = data.dropna(subset=['Date'])
                
                # Drop rows with invalid or missing 'Adj Close'
                data = data.dropna(subset=['Adj Close'])
                
                # Calculate daily returns
                returns = data[['Date', 'Adj Close']].copy()
                returns['Daily Return'] = returns['Adj Close'].pct_change().dropna()
                
                # Save the preprocessed data
                returns = returns.dropna(subset=['Daily Return'])
                returns.to_csv(output_file, index=False, columns=['Date', 'Daily Return'])
                print(f"Preprocessed data for {file_name} saved to {output_file}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

if __name__ == "__main__":
    # Define input and output directories
    input_dir = os.path.join(os.path.dirname(__file__), "../data/crypto")
    output_dir = os.path.join(os.path.dirname(__file__), "../data/prep")
    
    # Preprocess the data
    preprocess_crypto_data(input_dir, output_dir)