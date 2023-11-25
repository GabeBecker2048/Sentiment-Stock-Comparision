import csv
from gnews import GNews
from datetime import datetime

MAX_RESULTS = 20
with open("searchterms.txt", "r") as searchfile:
    NEWS_SEARCHES = searchfile.readlines()
    for i in range(len(NEWS_SEARCHES)):
        NEWS_SEARCHES[i] = NEWS_SEARCHES[i][:-1]
    
print(NEWS_SEARCHES)


# Configuration
news = GNews()
news.max_results = MAX_RESULTS

# Searching and saving
csv_data = []
for search in NEWS_SEARCHES:
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

    # Fill the remaining columns with empty strings if there are fewer than MAX_RESULTS articles
    row += ['', ''] * (MAX_RESULTS - len(inews))

    csv_data.append(row)

# Writing to CSV file
csv_header = ['Search Term']
for i in range(MAX_RESULTS):
    csv_header.extend([f"article {i + 1}", f"date {i + 1}"])

with open("Big7.csv", "w", newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_header)
    csv_writer.writerows(csv_data)
