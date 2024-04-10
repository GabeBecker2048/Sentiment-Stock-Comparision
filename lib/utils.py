import csv
import subprocess
import warnings
from datetime import datetime
from gnews import GNews
import yfinance as yf

from lib.settings import Settings


# This function runs an R Script in Python
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

    try:
        print("Generating articles...", file=outstream)

        # Configuration
        news = GNews()
        news.max_results = settings["NumArticles"]

        # before iterating through the search terms, we must first see what the maximum number of articles is:
        max_articles = max(len(searchlist) for searchlist in settings["SearchTerms"].values()) * settings["NumArticles"]

        # Searching and saving
        csv_data = []
        for searchlist in settings["SearchTerms"].values():
            row = [searchlist[0]]
            for search in searchlist:

                print(f"\n\tGenerating news for the search {search}...\n", file=outstream)
                inews = news.get_news(search)

                for article in inews:
                    title = article["title"].replace(',', '')

                    # if the article is already in the row, we continue to the next article
                    if title in row:
                        continue

                    date_str = article["published date"].replace(',', '')

                    # Format date to a more readable form
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        formatted_date = date_str

                    row += [title, formatted_date]
                    print(f"{title} - {formatted_date}, ", file=outstream)

            # Fill the remaining columns with empty strings if there are fewer than max_articles articles
            row += [' '] * (1 + (max_articles * 2) - len(row))

            csv_data.append(row)

        # Writing to CSV file
        csv_header = ['Search Term']
        for i in range(max_articles):
            csv_header += [f"article {i + 1}", f"date {i + 1}"]

        newsfile = f"./lib/csv_data/news_data/news_{datetime.now().strftime('%Y-%m-%d')}.csv"
        print(f"\nNews articles generated! Saving articles to: {newsfile}", file=outstream)
        with open(newsfile, "w", newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(csv_header)
            csv_writer.writerows(csv_data)

        print("Articles saved!\n", file=outstream)

    except Exception as e:
        print(f"Error: {e}\n", file=outstream)


def generate_sentiment_report(settings: Settings, outstream=None, gen_articles: bool = True):

    try:
        # generates the articles before generating the sentiment report
        if gen_articles:
            generate_articles(settings, outstream)

        print("Generating Sentiment report...\n", file=outstream)

        # the two paths to the R scripts
        r_script_path1 = './lib/RScripts/sentiment_analysis.R'
        r_script_path2 = './lib/RScripts/graph_sentiment.R'

        run_R_Script(r_script_path1, settings["RScriptLocation"], outstream)
        run_R_Script(r_script_path2, settings["RScriptLocation"], outstream)

        print("Finished Sentiment Report!\n", file=outstream)

    except Exception as e:
        print(f"Error: {e}", file=outstream)


def generate_stock_report(settings: Settings, outstream=None):

    try:
        print("Generating Stock Report...\n", file=outstream)

        # Initialize lists for current and previous day prices
        current_prices = []
        previous_prices = []
        differences = []

        # Iterate over stocks
        warnings.simplefilter(action='ignore', category=FutureWarning)
        for stock_symbol, stock_name in settings["SearchTerms"].items():
            ticker = yf.Ticker(stock_symbol)
            print(f"Getting data for {stock_symbol} - {stock_name[0]}...", file=outstream)

            # Get historical market data for the last 5 days
            hist = ticker.history(period="5d")

            # Check if there are enough data points
            if len(hist) < 2:
                print(f"Not enough data for {stock_name[0]}\n", file=outstream)
                # Append NaN to list
                previous_prices.append("NaN")
                current_prices.append("NaN")
                differences.append("NaN")
                continue

            # Get the last two days' prices
            previous_price = hist['Close'].iloc[-2]
            current_price = hist['Close'].iloc[-1]
            difference = current_price - previous_price
            print(f"Daily difference: {difference}\n", file=outstream)

            # Append prices to lists
            previous_prices.append(previous_price)
            current_prices.append(current_price)
            differences.append(difference)

        file_name = f"./lib/csv_data/stock_data/prices_{datetime.now().strftime('%Y-%m-%d')}.csv"

        print(f"Finished generating stock data! Saving to {file_name}\n", file=outstream)
        with open(file_name, "w", newline='') as f:
            w = csv.writer(f, delimiter=",", lineterminator='\r\n')
            w.writerow(("Ticker", "Open", "Close", "Difference"))
            for values in zip(settings["SearchTerms"], previous_prices, current_prices, differences):
                w.writerow(values)

        print(f'\nSuccessfully created stock data as {file_name}', file=outstream)

        print(f"Creating correlation analysis...", file=outstream)
        rscript_path = "./lib/RScripts/stock_analysis.R"
        run_R_Script(rscript_path, settings["RScriptLocation"], outstream)

        print("Finished stock report!", file=outstream)

    except Exception as e:
        print(f"Error: {e}", file=outstream)


def run_all(settings: Settings, outstream=None):
    generate_sentiment_report(settings, outstream)
    generate_stock_report(settings, outstream)
    print("Finished with daily report!", file=outstream)
