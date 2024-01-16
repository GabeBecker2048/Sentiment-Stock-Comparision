import csv
import subprocess
from gnews import GNews
from datetime import datetime, date

from lib.settings import Settings


def generate_articles(settings: Settings):
    print("Generating articles...\n")

    # Configuration
    news = GNews()
    news.max_results = settings["NumArticles"]
    
    # Searching and saving
    csv_data = []
    for search in settings["SearchTerms"].keys():

        print(f"\t\nGenerating news for {search}...\n")
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
            print(f"{title} - {formatted_date}, ")
        print('\n')

        # Fill the remaining columns with empty strings if there are fewer than settings["NumArticles"] articles
        row += ['', ''] * (settings["NumArticles"] - len(inews))
    
        csv_data.append(row)
    
    # Writing to CSV file
    csv_header = ['Search Term']
    for i in range(settings.s["NumArticles"]):
        csv_header.extend([f"article {i + 1}", f"date {i + 1}"])


    print(f"Saving articles to: './lib/csv_data/Top50_{str(date.today())}.csv'")
    with open(f"./lib/csv_data/Top50_{date.today()}.csv", "w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_data)

    print("Articles Generated!\n")


def generate_sentiment_report(settings: Settings):

    try:
        generate_articles(settings)

        print("\nGenerating Sentiment report...\n")

        # the two paths to the R scripts
        r_script_path1 = './lib/RScripts/sentiment_analysis.R'
        r_script_path2 = './lib/RScripts/graph_sentiment.R'

        print("\tRunning R Script 1...\n")

        # Run the R script using subprocess
        process = subprocess.Popen([settings.s["RScriptLocation"], r_script_path1],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # wait for process to finish
        out, errors = process.communicate()
        print(f"Output: {out}\n")
        print(f"Errors: {errors}\n")

        print("\tRunning R Script 2...\n")

        # Run the R script using subprocess
        process = subprocess.Popen([settings.s["RScriptLocation"], r_script_path2],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # wait for process to finish
        out, errors = process.communicate()
        print(f"Output: {out}\n")
        print(f"Errors: {errors}\n")

        print("R Scripts finished!\n")

    except Exception as e:
        print(f"Error: {e}")
