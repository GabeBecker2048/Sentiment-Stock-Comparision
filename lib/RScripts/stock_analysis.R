library(dplyr)
# Generate today's date in the desired format
today_date <- format(Sys.Date(), "%Y-%m-%d")

# Read the CSV file with today's date in the file path
file_path <- paste("./lib/csv_data/sentiment_data/sentiment_analysis_",today_date, ".csv", sep = "")
sentiment_analysis_dataset<- read.csv(file_path)

#Read the csv stock data
file_path <- paste("./lib/csv_data/stock_data/prices_",today_date, ".csv", sep = "")
stock_dataset<-read.csv(file_path)
stock_dataset_ordered<- stock_dataset[order(stock_dataset$V1),]

coorelation_dataset<-data.frame(
  Company = c(stock_dataset_ordered$V1),
  Old_Price = c(stock_dataset_ordered$V2),
  New_Price = c(stock_dataset_ordered$V3),
  Price_Change = c(stock_dataset_ordered$V4),
  Percent_Change =c(stock_dataset$V4/stock_dataset_ordered$V2),
  Sentiment_Score = c(sentiment_analysis_dataset$sentiment_score)
)

head(coorelation_dataset)

write.csv(coorelation_dataset, paste("./lib/csv_data/stock_analysis/stock_analysis_", today_date, ".csv", sep = ""))

#percent_change<-c(coorelation_dataset$X0.3300018310546875/coorelation_dataset$V2)
