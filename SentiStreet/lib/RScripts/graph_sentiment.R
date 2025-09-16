# Load required libraries
library(dplyr)
library(tidytext)
library(ggplot2)
library(tidyr)

# Generate today's date in the desired format
today_date <- format(Sys.Date(), "%Y-%m-%d")

# Read the CSV file with today's date in the file path
file_path <- paste("./lib/csv_data/sentiment_data/sentiment_", today_date, ".csv", sep = "")
sentiment_analysis_top50 <- read.csv(file_path)

# Plot using ggplot
ggplot(sentiment_analysis_top50, aes(x = Search.Term, y = sentiment_score, fill = sentiment_score)) +
  geom_bar(stat = "identity") +
  scale_fill_gradient(low = "red", high = "green") +
  ggtitle("Public Sentiment Score of 50 wealthy companies") +
  theme(axis.text.x = element_text(angle = 80, hjust = 1))

# Save the ggplot as an image in the ./lib/graphs/ directory with today's date
ggsave(paste("./lib/graphs/sentiment_", today_date, ".png", sep = ""), width = 10, height = 4)