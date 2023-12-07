""" Python Libraries """
import pandas as pd
import numpy as np



""" Function to read INL file """
def read_file(serinus_file):
    with open(serinus_file, 'r', encoding='ISO-8859-1') as file:
        content = file.readlines()
    data = []
    for line in content:
        values = line.strip().split()
        data.append(values)
    df = pd.DataFrame(data)
    df = df.iloc[1:]
    df.reset_index(drop=True, inplace=True)
    return(df)


""" Function to add headers to the data set """
def add_headers(serinus_data):
    serinus_data.columns = ['Date','Time','H2(PPM)','Diag1','Diag2','Diag3',
                        'Diag4','Diag5','Diag6','Diag7','Diag8','Diag9',
                        'Diag10','Diag11','Diag12','RTD Temp(C)', 'Voltage', 
                        'Sensor Temp (C)','%Humidity', 'Air Pressure (hPa)','USB Voltage']
    return serinus_data


""" Function that will remove the rows from the dataset where the timestamp is less than AnD dataset """
def remove_rows(sernius_data):
    df = sernius_data                                                            # Create a new dataframe
    index = df[sernius_data['Time'] >= '09:02:48'].index[0]                      # Find index of desired time stamp
    df = df.loc[index:]                                                          # Keep rows from the desired timestamp onwards
    return df                                                                    # Return new dataframe



""" Function to add 10Hz incremented time column """
def add_time(serinus_data):
    num_rows = len(serinus_data)                                 # Number of rows present in the dataset
    starting_time = 0                                            # Starting time in seconds
    time_increment = 1 / 10                                      # 10 Hz means 1/10 seconds per increment

    serinus_data['Test Time'] = np.linspace(starting_time, starting_time + (num_rows - 1) * time_increment, num_rows)
    return serinus_data




""" Function time to minutes """
def convert_time(serinus_data):
    serinus_data['Test Time'] = serinus_data['Test Time'] / 60
    return serinus_data


