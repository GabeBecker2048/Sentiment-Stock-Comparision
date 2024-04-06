library(dplyr)
library(ggplot2)
# Generate today's date in the desired format
today_date <- format(Sys.Date(), "%Y-%m-%d")

# Read the CSV file with today's date in the file path
file_path <- paste("../csv_data/sentiment_data/sentiment_",today_date, ".csv", sep = "")
sentiment_analysis_dataset<- read.csv(file_path)

#Read the csv stock data
file_path <- paste("../csv_data/stock_data/prices_",today_date, ".csv", sep = "")
stock_dataset<-read.csv(file_path)

stock_dataset_ordered<- stock_dataset[order(stock_dataset$Ticker),]

coorelation_dataset<-data.frame(
  Company = c(stock_dataset_ordered$Ticker),
  Old_Price = c(stock_dataset_ordered$Open),
  New_Price = c(stock_dataset_ordered$Close),
  Price_Change = c(stock_dataset_ordered$Difference),
  Percent_Change =c(stock_dataset$Difference/stock_dataset_ordered$Open),
  Sentiment_Score = c(sentiment_analysis_dataset$sentiment_score)
)

coorelation_dataset_filtered<-coorelation_dataset%>%
  filter(Percent_Change<1000000,Percent_Change>-10000000)
cor.test(coorelation_dataset_filtered$Percent_Change,coorelation_dataset_filtered$Sentiment_Score)

correlation_test_result <- cor.test(
  coorelation_dataset_filtered$Percent_Change,
  coorelation_dataset_filtered$Sentiment_Score
)

output_data <- data.frame(
  Estimate = correlation_test_result$estimate,
  P_Value = correlation_test_result$p.value,
  Method = correlation_test_result$method,
  Conf_Interval_Lower = correlation_test_result$conf.int[1],
  Conf_Interval_Upper = correlation_test_result$conf.int[2],
  Date = date(),
  Search_Terms = paste(coorelation_dataset_filtered$Company, collapse = ", ")
)
write.csv(output_data, file = paste("./lib/csv_data/coorelation_",today_date,".csv",sep = ""), row.names = FALSE)

ggplot(coorelation_dataset_filtered, aes(x=Sentiment_Score, y=Percent_Change))+ geom_point()+geom_smooth(method=lm)+xlab("Sentiment Score")+ylab("Percent Daily Change")

#ggsave(coorelation_dataset_filtered,paste("./lib/graphs/scatterplot_", today_date, ".png", sep = ""), width = 10, height = 4)


