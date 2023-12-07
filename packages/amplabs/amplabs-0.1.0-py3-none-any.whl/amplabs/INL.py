""" Python Libraries """
import pandas as pd
import numpy as np
from datetime import datetime



""" Function to read INL file """
def read_file(inl_file):
    df = pd.read_csv(inl_file, sep=',')
    tab_columns = ['Date', 'Time']                                           # Remove trailing tabs from specific columns
    df[tab_columns] = df[tab_columns].apply(lambda x: x.str.strip('\t'))
    return(df)                                                               # Return the clean data


""" Function that will remove the rows from the dataset where the timestamp is less than AnD dataset """
def remove_rows(inl_data):
    df = inl_data                                                            # Create a new dataframe
    index = df[inl_data['Time'] >= '9:02:48'].index[0]                       # Find index of desired time stamp
    df = df.loc[index:]                                                      # Keep rows from the desired timestamp onwards
    return df                                                                # Return new dataframe


""" Function to convert timestamp to seconds """
def convert_timestamp(inl_data):
    def datetime_to_seconds(date, time):                                     # Function to convert date and time to seconds
        dt_str = f"{date} {time}"
        dt = datetime.strptime(dt_str, '%m/%d/%Y %I:%M:%S %p')
        total_seconds = dt.timestamp()
        return total_seconds
                                                                             # Adding new column as test time in data
    inl_data['Test Time'] = inl_data.apply(lambda row: datetime_to_seconds(row['Date'], row['Time']), axis=1)
    start_time = inl_data['Test Time'].iloc[0]
    inl_data['Test Time']=inl_data['Test Time'].sub(start_time) 
    return inl_data



""" Function time to minutes """
def convert_time(inl_data):
    inl_data["Test Time"] = pd.to_numeric(inl_data["Test Time"]) / 60
    return inl_data

