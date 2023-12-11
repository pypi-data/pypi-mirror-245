import pandas as pd
import numpy as np
from datetime import datetime



def minutesToSeconds(column):
    column = pd.to_numeric(column) / 60
    return column



def showHeaders(df):
    headers = []
    for col in df.columns:                                               
        headers.append(col)
    return headers      


def convertToExcel(df, file_path):
    df.to_excel(file_path, index=False, engine='openpyxl')



def addHeaders(df, column_list):
    df.columns = column_list
    return df


def check_list_type(variable):
    if isinstance(variable, list):
        if all(isinstance(item, list) for item in variable):
            return "list_of_list"
        else:
            return "list"
    else:
        return "not_a_list"
    


def addTestTime(df, start_time, increment):
    num_rows = len(df)                                 # Number of rows present in the dataset

    df['Test Time'] = np.linspace(start_time, start_time + (num_rows - 1) * increment, num_rows)
    return df

