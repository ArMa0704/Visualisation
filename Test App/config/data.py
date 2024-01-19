import pandas as pd

def load_data():

    # Load dataset into a DataFrame
    df = pd.read_csv("Data/Raw/all_data.csv")

    # TODO : data preprocessing

    return df