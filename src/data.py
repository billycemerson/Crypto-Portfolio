import yfinance as yf
import pandas as pd
import os
import time

def fetch_and_save_crypto_data(crypto_symbols, start_date, end_date, output_dir, delay=2):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for symbol in crypto_symbols:
        ticker = f"{symbol}-USD"
        print(f"Fetching data for {ticker}...")
        
        try:
            # Fetch data for the cryptocurrency
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
            
            # Reset the index to make 'Date' a column
            data.reset_index(inplace=True)
            
            # Reorder columns to match the desired structure
            data = data[['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
            
            # Add a 'Price' column (same as 'Adj Close' for simplicity)
            data.insert(1, 'Price', data['Adj Close'])
            
            # Save the data to a CSV file
            output_file = os.path.join(output_dir, f"{symbol}.csv")
            data.to_csv(output_file, index=False)
            print(f"Data for {ticker} saved to {output_file}")
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")
        
        # Introduce a delay to avoid rate-limiting
        time.sleep(delay)

if __name__ == "__main__":
    crypto_symbols = ["BTC", "ETH", "BNB", "XRP", "ADA", "DOGE", "SOL", "DOT", "MATIC", "LTC"]
    start_date = "2024-01-01"
    end_date = "2025-06-01"
    
    # Define the output directory
    output_dir = os.path.join(os.path.dirname(__file__), "../data/crypto")
    
    # Fetch and save data for each cryptocurrency
    fetch_and_save_crypto_data(crypto_symbols, start_date, end_date, output_dir)