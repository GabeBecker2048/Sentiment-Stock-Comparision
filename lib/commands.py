import csv
import subprocess
from gnews import GNews
from datetime import datetime, date
import tkinter as tk


class RedirectText:
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
        self.output.place(relx=0.5, rely=0.4, anchor=tk.N)

    def writelines(self, lines):
        for line in lines:
            self.write(line)


def generate_articles(settings: dict, output: RedirectText):
    output.write("Generating articles...\n")

    # Configuration
    news = GNews()
    news.max_results = settings["NumArticles"]
    
    # Searching and saving
    csv_data = []
    for search in settings["SearchTerms"]:

        output.write(f"\t\nGenerating news for {search}...\n")
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
            output.write(f"{title} + {formatted_date}, ")
        output.write('\n')

        # Fill the remaining columns with empty strings if there are fewer than settings["NumArticles"] articles
        row += ['', ''] * (settings["NumArticles"] - len(inews))
    
        csv_data.append(row)
    
    # Writing to CSV file
    csv_header = ['Search Term']
    for i in range(settings["NumArticles"]):
        csv_header.extend([f"article {i + 1}", f"date {i + 1}"])


    output.write(f"Saving articles to: './lib/csv_data/Top50_{str(date.today())}.csv'")
    with open(f"./lib/csv_data/Top50_{date.today()}.csv", "w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_data)

    output.write("Articles Generated!\n")


def generate_sentiment_report(settings: dict, output: RedirectText):

    try:
        #generate_articles(settings, output)

        output.write("\nGenerating Sentiment report...\n")

        # the two paths to the R scripts
        r_script_path1 = './lib/RScripts/sentiment_analysis.R'
        r_script_path2 = './lib/RScripts/graph_sentiment.R'

        output.write("\tRunning R Script 1...\n")

        # Run the R script using subprocess
        process = subprocess.Popen([settings["RScriptLocation"], r_script_path1],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # wait for process to finish
        out, errors = process.communicate()
        output.write(f"Output: {out}\n")
        output.write(f"Errors: {errors}\n")

        output.write("\tRunning R Script 2...\n")

        # Run the R script using subprocess
        process = subprocess.Popen([settings["RScriptLocation"], r_script_path2],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # wait for process to finish
        out, errors = process.communicate()
        output.write(f"Output: {out}\n")
        output.write(f"Errors: {errors}\n")

        output.write("R Scripts finished!\n")

    except Exception as e:
        output.write(f"Error: {e}")
