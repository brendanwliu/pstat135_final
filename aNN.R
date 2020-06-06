library(dplyr)
library(neuralnet)
setwd("/media/brendanliu/1ffe4965-0a76-4845-aedc-1929d41a1cde/pstat135_final")
NC_data <- subset(NOAA_NC_DAvg_training_data, select = -c(CLASS))

scale01 <- function(x){
  (x - min(x)) / (max(x) - min(x))
}

NC_data_num <- subset(NC_data, select = -c(date)) %>%
  mutate_all(scale01)

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
NN1_Train_SSE <- sum((NC_NN1$net.result[[5]] - subset(train, select = c(Temp)))^2)/2
## Test Error
Test_NN1_Output <- compute(NC_NN1, test[, 0:25])$net.result
NN1_Test_SSE <- sum((Test_NN1_Output - subset(test, select = c(Temp)))^2)/2

