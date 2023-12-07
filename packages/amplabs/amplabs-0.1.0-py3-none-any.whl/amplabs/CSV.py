import pandas as pd

""" Function to read csv file """
def read_file(csv_file):
    df = pd.read_csv(csv_file)
    return df
