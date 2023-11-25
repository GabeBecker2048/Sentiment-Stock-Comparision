import csv
import json
from gnews import GNews
from datetime import datetime


def generate_articles(settings: dict):
    print("Generating Report with the following Settings:")
    print(settings)

    # Configuration
    news = GNews()
    news.max_results = settings["NumArticles"]
    
    # Searching and saving
    csv_data = []
    for search in settings["SearchTerms"]:
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
    
        # Fill the remaining columns with empty strings if there are fewer than settings["NumArticles"] articles
        row += ['', ''] * (settings["NumArticles"] - len(inews))
    
        csv_data.append(row)
    
    # Writing to CSV file
    csv_header = ['Search Term']
    for i in range(settings["NumArticles"]):
        csv_header.extend([f"article {i + 1}", f"date {i + 1}"])
    
    with open("Top50.csv", "w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_data)

    print("Report Generated!")

