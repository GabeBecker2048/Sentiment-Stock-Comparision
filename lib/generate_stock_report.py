import csv
import warnings
from datetime import datetime
import yfinance as yf
from settings import Settings
import sys

def generate_stock_report(settings, outstream=sys.stdout):
    print("Generating Stock Report...\n", file=outstream)
    previous_prices = []
    current_prices = []
    differences = []
    warnings.simplefilter(action="ignore", category=FutureWarning)
    
    for stock_symbol, stock_name in settings["SearchTerms"].items():
        ticker = yf.Ticker(stock_symbol)
        
        #print(f"Getting data for {stock_symbol} - {stock_name[0]}...", file=outstream)
        hist = ticker.history(period="5d")
        
        if len(hist) < 2:
            print(f"Not enough data for {stock_name[0]}\n", file=outstream)
            previous_prices.append("NaN")
            current_prices.append("NaN")
            differences.append("NaN")
            continue
        
        previous_price = hist["Close"].iloc[-2]
        current_price = hist["Close"].iloc[-1]
        difference = current_price - previous_price
        #print(f"Daily difference: {difference}\n", file=outstream)
        
        previous_prices.append(previous_price)
        current_prices.append(current_price)
        differences.append(difference)
    
    file_name = f"./lib/csv_data/stock_data/prices_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    print(f"Finished generating stock data! Saving to {file_name}\n", file=outstream)
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\r\n")
        writer.writerow(("Ticker", "Open", "Close", "Difference"))
        for values in zip(settings["SearchTerms"], previous_prices, current_prices, differences):
            writer.writerow(values)
    print(f"\nSuccessfully created stock data as {file_name}", file=outstream)

def main():
    settings = Settings('./lib/settings.json')
    generate_stock_report(settings)

if __name__ == "__main__":
    main()
