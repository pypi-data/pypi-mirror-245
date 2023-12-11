""" Python Libraries """
import pandas as pd
from nptdms import TdmsFile
import numpy as np



""" Function to read BADgE file """
def read_file(BADgE_file):
    tdms_file = TdmsFile.read(BADgE_file, True)                                 # Read TDMS file
    df = tdms_file.as_dataframe(True)
    channel_data_dict = {}
    max_length = 0

    for group in tdms_file.groups():                                         # Get group, channel and channel data from the file
        for channel in group.channels():
            channel_data = channel[:]
            if len(channel_data) > max_length:
                max_length = len(channel_data)
            channel_data_dict[channel.name] = channel_data

    for channel_name, channel_data in channel_data_dict.items():             # Pad the channel data with NaN to match the maximum length
        if len(channel_data) < max_length:
            channel_data_dict[channel_name] = np.concatenate((channel_data, [np.nan] * (max_length - len(channel_data))))

    df = pd.DataFrame(channel_data_dict)                                     # Create a dataframe from the channel data
    df.columns = [col.replace('\n', ' ') for col in df.columns]

    channel = group['Amphenol']
    timestamps = channel.time_track()                                        # Calculate the time stamp
    df['Time Track'] = timestamps                                            # Add time stamp to the channel data

    return df                                                                # Return the final dataframe



""" Function to convert BADgE data to excel """
def convert_to_excel(BADgE_data, excel_BADgE_file):
    BADgE_data.to_excel(excel_BADgE_file, index=False, engine='openpyxl')



""" Function that will remove the rows from the dataset where the timestamp is less than AnD dataset """
def remove_rows(BADgE_data):
    df = BADgE_data                                                           # Create a new dataframe
    index = df[BADgE_data['Time Track'] >= 90.0].index[0]                     # Find index of desired time stamp
    df = df.loc[index:]                                                       # Keep rows from the desired timestamp onwards
    return df                                                                 # Return new dataframe




""" Function to add incremented time column """
def add_test_time(BADgE_data):
    num_rows = len(BADgE_data)                                                # Number of rows present in the dataset
    starting_time = 0                                                         # Starting time in seconds
    time_increment = .1                                                       # 0.1 Hz increment

    BADgE_data['Test Time'] = np.linspace(starting_time, starting_time + (num_rows - 1) * time_increment, num_rows)
    BADgE_data['Test Time'] = BADgE_data['Test Time'] / 60
    return BADgE_data



""" Function to calculate and add CAN timing """
def add_can_time(BADgE_data):
    analog_data_points = len(BADgE_data)                                            # Count of analog data points
                                                                                    # Count the length of the 'Values' column until the first NaN
    first_nan_index = BADgE_data['Ethanol BSS_V7'].index[BADgE_data['Ethanol BSS_V7'].isnull()].tolist()[0]
    can_data_points = BADgE_data['Ethanol BSS_V7'].iloc[:first_nan_index].count()   
    
    BADgE_data['CAN Time'] = np.arange(0, len(BADgE_data) * 0.1, 0.1)               # Create Time scale
    ratio = can_data_points / analog_data_points                                    # Calculate ratio
    BADgE_data['CAN Time'] = BADgE_data['CAN Time'] * ratio                         # Calculate CAN time
    BADgE_data['CAN Time'] = BADgE_data['CAN Time'] / 60                            # Convert time into minute
    return BADgE_data

