import yfinance as yf
from datetime import datetime, timedelta
import csv

# Dictionary of stocks
stocks_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta Platforms (Facebook)": "META",
    "Berkshire Hathaway": "BRK.B",
    "Tesla": "TSLA",
    "Eli Lilly": "LLY",
    "Visa": "V",
    "Broadcom": "AVGO",
    "UnitedHealth": "UNH",
    "JPMorgan Chase": "JPM",
    "Walmart": "WMT",
    "Exxon Mobil": "XOM",
    "Mastercard": "MA",
    "Johnson & Johnson": "JNJ",
    "Procter & Gamble": "PG",
    "Oracle": "ORCL",
    "Home Depot": "HD",
    "Adobe": "ADBE",
    "Chevron": "CVX",
    "Costco": "COST",
    "Merck": "MRK",
    "Coca-Cola": "KO",
    "AbbVie": "ABBV",
    "Bank of America": "BAC",
    "Pepsico": "PEP",
    "Salesforce": "CRM",
    "Netflix": "NFLX",
    "McDonald": "MCD",
    "AMD": "AMD",
    "Cisco": "CSCO",
    "Thermo Fisher Scientific": "TMO",
    "Intel": "INTC",
    "Abbott Laboratories": "ABT",
    "T-Mobile US": "TMUS",
    "Pfizer": "PFE",
    "Comcast": "CMCSA",
    "Walt Disney": "DIS",
    "Nike": "NKE",
    "Danaher": "DHR",
    "Intuit": "INTU",
    "Verizon": "VZ",
    "Wells Fargo": "WFC",
    "Philip Morris": "PM",
    "QUALCOMM": "QCOM",
    "Amgen": "AMGN",
    "IBM": "IBM",
    "Texas Instruments": "TXN"
}

# Get today's date and the date five days ago
today = datetime.now()
five_days_ago = today - timedelta(days=5)

# Format dates for yfinance
today_str = today.strftime('%Y-%m-%d')
five_days_ago_str = five_days_ago.strftime('%Y-%m-%d')

# Initialize lists for current and previous day prices
current_prices = []
previous_prices = []
differences = []

# Iterate over stocks
for stock_name, stock_symbol in stocks_dict.items():
    ticker = yf.Ticker(stock_symbol)

    # Get historical market data for the last 5 days
    hist = ticker.history(start=five_days_ago_str, end=today_str)

    # Check if there are enough data points
    if len(hist) < 2:
        print(f"Not enough data for {stock_name}")
        # Append zeros to lists
        previous_prices.append(0)
        current_prices.append(0)
        differences.append(0)
        continue

    # Get the last two days' prices
    previous_price = hist['Close'].iloc[-2]
    current_price = hist['Close'].iloc[-1]
    difference = current_price - previous_price

    # Append prices to lists
    previous_prices.append((previous_price))
    current_prices.append((current_price))
    differences.append((current_price - previous_price))


print('PREVIOUS DAY PRICES: ', previous_prices)
print('CURRENT PRICES: ', current_prices)
print('DIFFERENCES: ', differences)

with open("prices.csv", "w", newline='') as f:
    w = csv.writer(f, delimiter=",", lineterminator='\r\n')
    for values in zip(stocks_dict, previous_prices, current_prices, differences):
        w.writerow(values)
