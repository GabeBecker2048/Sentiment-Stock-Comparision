import pandas as pd
from transformers import pipeline
import datetime
import csv
import math

# Generate today's date in the desired format
today_date = datetime.date.today().strftime("%Y-%m-%d")

# Read the CSV file with today's date in the file path
file_path = f"./lib/csv_data/news_data/news_{today_date}.csv"
df = pd.read_csv(file_path)

# Identify article text columns (assumed columns start with "article")
article_cols = [col for col in df.columns if col.startswith("article")]

# Initialize sentiment analysis pipeline using transformers
sa_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# Initialize global trackers
global_max_intensity = -math.inf
global_max_article = ""
global_min_intensity = math.inf
global_min_article = ""
row_summaries = []

results = []
for _, row in df.iterrows():
    search_term = row["Search Term"]
    pos_count = 0
    pos_intensity = 0
    neg_count = 0
    neg_intensity = 0
    # Initialize per-row tracker
    row_max_intensity = -math.inf
    row_max_article = ""
    
    for col in article_cols:
        article = row[col]
        if pd.isna(article) or not str(article).strip():
            continue
        # Process full headline (strip whitespace)
        text = str(article).strip()
        #print(text)
        result = sa_pipeline(text)[0]
        #print(result)
        score = result["score"]
        
        # Update counts and intensities
        if result["label"] == "positive":
            pos_count += 1
            pos_intensity += score
        if result["label"] == "negative":
            neg_count += 1
            neg_intensity += score
        
        # Update global max/min intensity articles
        if score > global_max_intensity:
            global_max_intensity = score
            global_max_article = text
        if score < global_min_intensity:
            global_min_intensity = score
            global_min_article = text
        
        # Update row-specific max intensity article
        if score > row_max_intensity:
            row_max_intensity = score
            row_max_article = text

    sentiment_score = pos_count - neg_count
    intensity_score = pos_intensity - neg_intensity
    results.append({
        "Search Term": search_term,
        "negative": neg_count,
        "positive": pos_count,
        "sentiment_score": sentiment_score,
        "sentiment_intensity": intensity_score
    })
    # Save row summary for later use
    row_summaries.append({
        "Search Term": search_term,
        "sentiment_score": sentiment_score,
        "row_max_intensity": row_max_intensity,
        "row_max_article": row_max_article
    })

result_df = pd.DataFrame(results)
# Sort results alphabetically by search term
result_df = result_df.sort_values(by="Search Term")
# Set index starting at 1 and convert to string to ensure quoting
result_df.index = (result_df.index + 1).astype(str)

output_path = f"./lib/csv_data/sentiment_data/sentiment_{today_date}.csv"
result_df.to_csv(output_path, index=True, index_label="", quoting=csv.QUOTE_NONNUMERIC)

# Print global highest and lowest intensity articles
print("Article with highest intensity:", global_max_article)
print("Article highest intensity score:", global_max_intensity)  # New print for max score
print("Article with lowest intensity:", global_min_article)
print("Article lowest intensity score:", global_min_intensity)  # New print for min score

# Determine the company (row) with the highest sentiment score
max_sentiment = max(item["sentiment_score"] for item in row_summaries)
# Filter rows having the maximum sentiment score
max_sentiment_rows = [item for item in row_summaries if item["sentiment_score"] == max_sentiment]
# Among these, choose the one with highest row_max_intensity
selected = max(max_sentiment_rows, key=lambda x: x["row_max_intensity"])
print("For companies with the highest sentiment score, the article with the highest intensity is:")
print(selected["row_max_article"])
print("Score:", selected["row_max_intensity"])  # New print for highest sentiment company's article score

# Add: Print article with highest intensity for the company with the lowest sentiment score
min_sentiment = min(item["sentiment_score"] for item in row_summaries)
min_sentiment_rows = [item for item in row_summaries if item["sentiment_score"] == min_sentiment]
lowest_selected = max(min_sentiment_rows, key=lambda x: x["row_max_intensity"])
print("For companies with the lowest sentiment score, the article with the highest intensity is:")
print(lowest_selected["row_max_article"])
print("Score:", lowest_selected["row_max_intensity"])  # New print for lowest sentiment company's article score
