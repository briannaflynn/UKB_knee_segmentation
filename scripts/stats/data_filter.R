library(tidyverse)

right["x"]

iq.r <- function(dataframe, var) {
  
  df <- dataframe
  vec <- df[var]
  q1 <- quantile(vec, .25)
  q3 <- quantile(vec, .75)
  iqr_val <- IQR(vec)
  
  no_outliers <- subset(df, var > (q1 - 1.5 * iqr_val) & var < (q3 + 1.5 * iqr_val))
  return(no_outliers) 
}

right['q1.1']

nl <- iq.r(right, 'q1.1')
