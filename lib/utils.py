import csv
import subprocess
from datetime import datetime, timedelta
from gnews import GNews
import yfinance as yf

from lib.settings import Settings


def run_R_Script(r_script_path: str, RScriptLocation: str = "Rscript", outstream=None):
    print(f"\tRunning {r_script_path}...\n", file=outstream)

    # Run the R script using subprocess
    process = subprocess.Popen([RScriptLocation, r_script_path],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # wait for process to finish
    out, errors = process.communicate()
    print(f"Output: {out}\n", file=outstream)
    print(f"Errors: {errors}\n", file=outstream)

    print(f"\tFinished running {r_script_path}!\n", file=outstream)


def generate_articles(settings: Settings, outstream=None):
    print("Generating articles...\n", file=outstream)

    # Configuration
    news = GNews()
    news.max_results = settings["NumArticles"]
    
    # Searching and saving
    csv_data = []
    for searchlist in settings["SearchTerms"].values():
        for search in searchlist:

            print(f"\t\nGenerating news for the search {search}...\n", file=outstream)
            inews = news.get_news(search)
            row = [search]

            for article in inews:
                title = article["title"].replace(',', '')

                date_str = article["published date"].replace(',', '')

                # Format date to a more readable form
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    formatted_date = date_str

                row.extend([title, formatted_date])
                print(f"{title} - {formatted_date}, ", file=outstream)
            print('\n', file=outstream)

        # Fill the remaining columns with empty strings if there are fewer than settings["NumArticles"] articles
        row += ['', ''] * (settings["NumArticles"] - len(inews))
    
        csv_data.append(row)
    
    # Writing to CSV file
    csv_header = ['Search Term']
    for i in range(settings["NumArticles"]):
        csv_header.extend([f"article {i + 1}", f"date {i + 1}"])


    print(f"Saving articles to: './lib/csv_data/news_data/Top50_{datetime.now().strftime('%Y-%m-%d_%H')}.csv'", file=outstream)
    with open(f"./lib/csv_data/news_data/Top50_{datetime.now().strftime('%Y-%m-%d_%H')}.csv", "w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_data)

    print("Articles Generated!\n", file=outstream)


def generate_sentiment_report(settings: Settings, outstream=None, gen_articles: bool = True):

    try:
        # generates the articles before generating the sentiment report
        if gen_articles:
            generate_articles(settings, outstream)

        print("\nGenerating Sentiment report...\n", file=outstream)

        # the two paths to the R scripts
        r_script_path1 = './lib/RScripts/sentiment_analysis.R'
        r_script_path2 = './lib/RScripts/graph_sentiment.R'

        run_R_Script(r_script_path1, settings["RScriptLocation"], outstream)
        run_R_Script(r_script_path2, settings["RScriptLocation"], outstream)

        print("R Scripts finished!\n", file=outstream)

    except Exception as e:
        print(f"Error: {e}", file=outstream)


def generate_stock_report(settings: Settings, outstream=None):
    print("Generating Stock Report...\n", file=outstream)

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
    for stock_symbol, stock_name in settings["SearchTerms"].items():
        ticker = yf.Ticker(stock_symbol)

        # Get historical market data for the last 5 days
        hist = ticker.history(start=five_days_ago_str, end=today_str)

        # Check if there are enough data points
        if len(hist) < 2:
            print(f"Not enough data for {stock_name}", file=outstream)
            # Append zeros to lists
            previous_prices.append("NaN")
            current_prices.append("NaN")
            differences.append("NaN")
            continue

        # Get the last two days' prices
        previous_price = hist['Close'].iloc[-2]
        current_price = hist['Close'].iloc[-1]
        difference = current_price - previous_price

        # Append prices to lists
        previous_prices.append(previous_price)
        current_prices.append(current_price)
        differences.append(difference)

    print('PREVIOUS DAY PRICES: ', previous_prices, file=outstream)
    print('CURRENT PRICES: ', current_prices, file=outstream)
    print('DIFFERENCES: ', differences, file=outstream)

    file_name = f"./lib/csv_data/stock_data/prices_{datetime.now().strftime('%Y-%m-%d_%H')}.csv"

    with open(file_name, "w", newline='') as f:
        w = csv.writer(f, delimiter=",", lineterminator='\r\n')
        for values in zip(settings["SearchTerms"], previous_prices, current_prices, differences):
            w.writerow(values)

    print(f'\nSuccessfully created stock data as {file_name}', file=outstream)

    """
    print(f"Creating stock analysis...", file=outstream)
    rscript_path = "./lib/Rscipts/stock_analysis.R"
    run_R_Script(rscript_path, settings["RScriptLocation"], outstream)
    print("R scripts finished!", file=outstream)
    """

    print("Finished stock report!", file=outstream)

