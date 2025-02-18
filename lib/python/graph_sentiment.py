import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime

# ...existing code for setup if any...
today_date = datetime.date.today().strftime("%Y-%m-%d")

# Read the sentiment CSV
file_path = f"./lib/csv_data/sentiment_data/sentiment_{today_date}.csv"
df = pd.read_csv(file_path)

# Plot sentiment score
norm = mcolors.Normalize(vmin=df['sentiment_score'].min(), vmax=df['sentiment_score'].max())
cmap = plt.cm.RdYlGn
colors = cmap(norm(df['sentiment_score']))

plt.figure(figsize=(10, 4))
bars = plt.bar(df['Search Term'], df['sentiment_score'], color=colors)
plt.xticks(rotation=80, ha='right')
plt.title("Public Sentiment Score of 50 wealthy companies")
plt.xlabel("Search Term")
plt.ylabel("Sentiment Score")
plt.tight_layout()
plt.savefig(f"./lib/graphs/sentiment_{today_date}.png")
plt.close()

# Plot sentiment intensity
norm_intensity = mcolors.Normalize(vmin=df['sentiment_intensity'].min(), vmax=df['sentiment_intensity'].max())
colors_intensity = cmap(norm_intensity(df['sentiment_intensity']))

plt.figure(figsize=(10, 4))
bars = plt.bar(df['Search Term'], df['sentiment_intensity'], color=colors_intensity)
plt.xticks(rotation=80, ha='right')
plt.title("Public Sentiment Intensity of 50 wealthy companies")
plt.xlabel("Search Term")
plt.ylabel("Sentiment Intensity")
plt.tight_layout()
plt.savefig(f"./lib/graphs/sentiment_intensity_{today_date}.png")
plt.close()
