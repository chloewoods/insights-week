import pandas
import json


def read_data(name):
    """Read in a dataset.
    
    Args:
        name (str): Name of the dataset to read.
    
    Returns:
        `pandas.core.frame.DataFrame`
    
    """
    df = pandas.read_csv(f"../res/{name}.csv")
    return df


passengers = read_data("passengers")
family_info = read_data("family_info")
tickets = read_data("tickets")
test_passengers = read_data("test_passengers")
test_family_info = read_data("test_family_info")
test_tickets = read_data("test_tickets")


def percent_correct(prediction):
    """Get the percent of the predictions that are correct.

    Args:
        prediction (`pandas.core.frame.DataFrame`): Dataframe containing 
            your predictions in the column named 'prediction'.
    
    Returns:
        float: The percent of the predictions which are correct, between
            0 and 1 where 0.5 is equivalent to 50%.
    
    """
    if "prediction" not in list(prediction):
        raise KeyError(
            "The dataframe must contain the predictions in a column named "
            "'prediction'."
        )
    
    raw_truth = json.load(open("../res/truth.json"))
    truth = pandas.DataFrame(raw_truth, columns=["PassengerId", "truth"])
    both = prediction.merge(truth, on="PassengerId", how="inner")
    
    if len(both) != 223:
        raise Warning(
            "The dataframe is missing some passengers. There should be "
            "predictions for all 223."
        )
    
    correct = both["prediction"] == both["truth"]
    perc_correct = sum(correct) / len(both)
    return perc_correct