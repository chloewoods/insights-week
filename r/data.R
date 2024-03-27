library(data.table)
library(rjson)


#' Read in a dataset.
#' 
#' @param name Name of the dataset to read.
#' @return data.table.
read_data <- function(name) {
  dt <- fread(paste("../res/", name, ".csv", sep=""), na.strings="")
  return(dt)
}


passengers <- read_data("passengers")
family_info <- read_data("family_info")
tickets <- read_data("tickets")
test_passengers <- read_data("test_passengers")
test_family_info <- read_data("test_family_info")
test_tickets <- read_data("test_tickets")


#' Get the percent of the predictions that are correct.
#' 
#' @param prediction Dataframe containing your predictions in the column named 'prediction'.
#' @return The percent of the predictions which are correct, between 0 and 1 where 0.5 is equivalent to 50%.
percent_correct <- function(predictions) {
  if (!"prediction" %in% names(predictions)) {
    stop("The dataset must contain the predictions in a column named 'prediction'.")
  }
  
  raw_truth <- fromJSON(file="../res/truth.json")
  truth <- data.table(PassengerId=sapply(raw_truth, "[[", 1), truth=sapply(raw_truth, "[[", 2))
  both <- merge(predictions, truth, by="PassengerId", all=FALSE)
  
  if (nrow(both) != 223) {
    warning("The dataset is missing some passengers. There should be predictions for all 223.")
  }
  
  correct <- which(both$prediction == both$truth)
  perc_correct <- length(correct) / nrow(both)
  return(perc_correct)
}