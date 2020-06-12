library(dplyr)
library(neuralnet)
library(ggplot2)
library(GGally)
setwd("/media/brendanliu/1ffe4965-0a76-4845-aedc-1929d41a1cde/pstat135_final")
NC_data <- subset(NOAA_NC_DAvg_training_data, select = -c(CLASS, MinTemp, MaxTemp, MinBP, MaxBP, MinRH, MaxRH, MinWSpd, MaxWSpd, MaxTempT, MinTempT, MaxRHT, MinRHT, MaxBPT, MinBPT, MaxWSpdT, MinWSpdT))
ggcorr(subset(NOAA_NC_DAvg_training_data, select = -c(date,Temp, CLASS,MaxTempT, MinTempT, MaxRHT, MinRHT, MaxBPT, MinBPT, MaxWSpdT, MinWSpdT)))
scale01 <- function(x){
  (x - min(x)) / (max(x) - min(x))
}

NC_data_num <- subset(NC_data, select = -c(date)) %>%
  mutate_all(scale01)
ggpairs(NC_data_num)
set.seed(101)
# Set Seed so that same sample can be reproduced in future also
# Now Selecting 75% of data as sample from total 'n' rows of the data  
sample <- sample.int(n = nrow(NC_data_num), size = floor(.75*nrow(NC_data_num)), replace = F)
train <- NC_data_num[sample, ]
test  <- NC_data_num[-sample, ]


set.seed(12321)
NC_NN1 <- neuralnet(Temp~., 
                       data = train, 
                       hidden = c(10), 
                       act.fct = "logistic",
                       rep = 10)
plot(NC_NN1, rep = 'best', fontsize = 10, information = FALSE, intercept = FALSE)
NC_NN1$result.matrix[1,]
## Training Error
NN1_Train_SSE <- (sum((NC_NN1$net.result[[1]] - train$Temp)^2)/nrow(train))^0.5
## Test Error
Test_NN1_Output <- compute(NC_NN1, test[, 0:9])$net.result
NN1_Test_RMSE <- (sum((Test_NN1_Output - test$Temp)^2/nrow(test)))^0.5
ggplot(data = NULL) + geom_line(aes(x=1:nrow(Test_NN1_Output), y=Test_NN1_Output)) + geom_line(aes(x = 1:nrow(test), test$Temp), col = "red")

set.seed(12321)
NC_NN2 <- neuralnet(Temp~., 
                    data = train, 
                    hidden = c(32,5), 
                    act.fct = "logistic",
                    rep = 10)
plot(NC_NN2, rep = 'best', fontsize = 10, information = FALSE, intercept = FALSE)
NC_NN2$result.matrix[1,]
## Training Error
NN2_Train_SSE <- (sum((NC_NN2$net.result[[1]] - train$Temp)^2)/nrow(train))^0.5
## Test Error
Test_NN2_Output <- compute(NC_NN2, test[, 0:9])$net.result
NN2_Test_RMSE <- (sum((Test_NN2_Output - test$Temp)^2/nrow(test)))^0.5
