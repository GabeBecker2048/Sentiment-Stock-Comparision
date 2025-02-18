import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

today_date = datetime.date.today().strftime("%Y-%m-%d")

# Read sentiment data and stock data
sentiment_path = f"./lib/csv_data/sentiment_data/sentiment_{today_date}.csv"
sentiment_df = pd.read_csv(sentiment_path)

stock_path = f"./lib/csv_data/stock_data/prices_{today_date}.csv"
stock_df = pd.read_csv(stock_path)

# Order stock dataset by Ticker
stock_df_ordered = stock_df.sort_values(by="Ticker")

# Build correlation dataset using sentiment score
corr_df = pd.DataFrame({
    "Company": stock_df_ordered["Ticker"],
    "Old_Price": stock_df_ordered["Open"],
    "New_Price": stock_df_ordered["Close"],
    "Price_Change": stock_df_ordered["Difference"],
    "Percent_Change": stock_df_ordered["Difference"] / stock_df_ordered["Open"],
    "Sentiment_Score": sentiment_df["sentiment_score"]
})

# Filter dataset
corr_df_filtered = corr_df[(corr_df["Percent_Change"] < 1e6) & (corr_df["Percent_Change"] > -1e7)]

# Compute Pearson correlation and confidence intervals for sentiment score
r, p_value = stats.pearsonr(corr_df_filtered["Percent_Change"], corr_df_filtered["Sentiment_Score"])
n = len(corr_df_filtered)
if n > 3:
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    z_crit = 1.96
    lower_z = z - z_crit * se
    upper_z = z + z_crit * se
    ci_lower = np.tanh(lower_z)
    ci_upper = np.tanh(upper_z)
else:
    ci_lower, ci_upper = None, None

output_data = pd.DataFrame({
    "Estimate": [r],
    "P_Value": [p_value],
    "Method": ["Pearson's correlation"],
    "Conf_Interval_Lower": [ci_lower],
    "Conf_Interval_Upper": [ci_upper],
    "Date": [datetime.datetime.now().strftime("%Y-%m-%d")],
    "Search_Terms": [", ".join(corr_df_filtered["Company"].astype(str).tolist())]
})

output_path = f"./lib/csv_data/correlation_data/correlation_{today_date}.csv"
output_data.to_csv(output_path, index=False)

# Plot scatter with regression line for sentiment score
plt.figure(figsize=(10, 4))
sns.regplot(x="Sentiment_Score", y="Percent_Change", data=corr_df_filtered, ci=None, scatter_kws={'s':50})
plt.xlabel("Sentiment Score")
plt.ylabel("Percent Daily Change")
plt.tight_layout()
plt.savefig(f"./lib/graphs/correlation_{today_date}.png")
plt.close()
print(p_value)
if p_value < 0.05:
    print("Significant correlation found for Sentiment Score.")
else:
    print("No significant correlation found for Sentiment Score.")

# ----- Additional correlation analysis using sentiment intensity -----
# Build correlation dataset using sentiment intensity
corr_df_intensity = corr_df.copy()
corr_df_intensity["Sentiment_Intensity"] = sentiment_df["sentiment_intensity"]

# Compute Pearson correlation and confidence intervals for sentiment intensity
r_intensity, p_value_intensity = stats.pearsonr(corr_df_intensity["Percent_Change"], corr_df_intensity["Sentiment_Intensity"])
n_intensity = len(corr_df_intensity)
if n_intensity > 3:
    z_intensity = np.arctanh(r_intensity)
    se_intensity = 1 / np.sqrt(n_intensity - 3)
    z_crit = 1.96
    lower_z_intensity = z_intensity - z_crit * se_intensity
    upper_z_intensity = z_intensity + z_crit * se_intensity
    ci_lower_intensity = np.tanh(lower_z_intensity)
    ci_upper_intensity = np.tanh(upper_z_intensity)
else:
    ci_lower_intensity, ci_upper_intensity = None, None

output_data_intensity = pd.DataFrame({
    "Estimate": [r_intensity],
    "P_Value": [p_value_intensity],
    "Method": ["Pearson's correlation"],
    "Conf_Interval_Lower": [ci_lower_intensity],
    "Conf_Interval_Upper": [ci_upper_intensity],
    "Date": [datetime.datetime.now().strftime("%Y-%m-%d")],
    "Search_Terms": [", ".join(corr_df_intensity["Company"].astype(str).tolist())]
})

correlation_intensity_output_path = f"./lib/csv_data/correlation_data/correlation_intensity_{today_date}.csv"
output_data_intensity.to_csv(correlation_intensity_output_path, index=False)

# Plot scatter with regression line for sentiment intensity
plt.figure(figsize=(10, 4))
sns.regplot(x="Sentiment_Intensity", y="Percent_Change", data=corr_df_intensity, ci=None, scatter_kws={'s':50})
plt.xlabel("Sentiment Intensity")
plt.ylabel("Percent Daily Change")
plt.tight_layout()
plt.savefig(f"./lib/graphs/correlation_intensity_{today_date}.png")
plt.close()
print(p_value_intensity)
if p_value_intensity < 0.05:
    print("Significant correlation found for Sentiment Intensity.")
else:
    print("No significant correlation found for Sentiment Intensity.")
