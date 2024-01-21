# Load required libraries
library(dplyr)
library(tidytext)
library(ggplot2)
library(tidyr)

# Generate today's date in the desired format
today_date <- format(Sys.Date(), "%Y-%m-%d")

# Read the CSV file with today's date in the file path
file_path <- paste("./lib/csv_data/news_data/Top50_", today_date, ".csv", sep = "")
Top50 <- read.csv(file_path)

# Extract article titles and dates
article_titles <- c()
article_dates <- c()

i <- 2
while (i <= ncol(Top50)) {
  article_titles <- cbind(article_titles, Top50[, i])
  article_dates <- cbind(article_dates, Top50[, i + 1])
  i = i + 2
}

article_titles <- as.vector(article_titles)
article_dates <- as.vector(article_dates)

Top50_clean <- data.frame(Search.Term = Top50$Search.Term, article_dates, article_titles)

# Perform sentiment analysis
sentiment_analysis_top50 <- Top50_clean %>%
  unnest_tokens(word, article_titles) %>%
  inner_join(get_sentiments("bing")) %>%
  count(Search.Term, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  mutate(sentiment_score = positive - negative)

# Convert 'Search.Term' to a factor with specific levels
sentiment_analysis_top50$Search.Term <- factor(sentiment_analysis_top50$Search.Term, levels = unique(sentiment_analysis_top50$Search.Term))

write.csv(sentiment_analysis_top50, paste("./lib/csv_data/sentiment_data/sentiment_analysis_", today_date, ".csv", sep = ""))