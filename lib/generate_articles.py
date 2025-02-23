import csv
from datetime import datetime
from gnews import GNews
from settings import Settings
import sys

def generate_articles(settings, outstream=sys.stdout):
    print("Generating articles...")
    try:
        news = GNews()
        news.max_results = settings["NumArticles"]
        newsfile = f"./lib/csv_data/news_data/news_{datetime.now().strftime('%Y-%m-%d')}.csv"
        max_articles = max(len(searchlist) for searchlist in settings["SearchTerms"].values()) * settings["NumArticles"]
        csv_data = []

        for searchlist in settings["SearchTerms"].values():
            row = [searchlist[0]]
            
            for search in searchlist:
                print(f"\n\tGenerating news for the search {search}...\n", file=outstream)
                inews = news.get_news(search)
                
                for article in inews:
                    title = article["title"].replace(",", "")
                    if title in row:
                        continue
                    date_str = article["published date"].replace(",", "")
                    formatted_date = datetime.strptime(date_str, "%a %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d %H:%M:%S")
                    row += [title, formatted_date]
                    #print(f"{title} - {formatted_date}, ", file=outstream)
            
            row += [" "] * (1 + (max_articles * 2) - len(row))
            csv_data.append(row)
        
        csv_header = ["Search Term"] + [f"article {i+1}" for i in range(max_articles) for _ in (0,)]  # header for articles and dates
        # Alternatively, create header with article/date pairs:
        csv_header = ["Search Term"] + [f"article {i+1}" if j % 2 == 0 else f"date {i+1}" 
                                          for i in range(max_articles) for j in range(2)]
        
        print(f"\nNews articles generated! Saving articles to: {newsfile}", file=outstream)
        with open(newsfile, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(csv_header)
            csv_writer.writerows(csv_data)
        print("Articles saved!\n", file=outstream)
    
    except Exception as e:
        print(f"Error: {e}\n", file=outstream)

def main():
    settings = Settings('./lib/settings.json')
    generate_articles(settings)

if __name__ == "__main__":
    main()
