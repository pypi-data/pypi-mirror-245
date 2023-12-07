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

