""" Python Libraries """
import re
import pandas as pd


""" Function to read the dat file"""
def read_file(AnD_file):
    AnD_data = []

    regex_patterns = [                                                          # Define the regex patterns and replacements
        (re.compile(r"^(?!1).*.[\r\n|\n]", re.MULTILINE), ""),                  # Remove lines not starting with '1'
        (re.compile(r"^(1\t*ALIAS\t)", re.MULTILINE), ""),                      # Remove lines starting with '1 ALIAS'
        (re.compile(r"^(1.*DATA\t)", re.MULTILINE), ""),                        # Remove lines starting with '1 DATA'
        (re.compile(r"^(1.*PARAMS).*.[\r\n|\n]", re.MULTILINE), ""),            # Remove lines starting with '1 PARAMS'
        (re.compile(r"^(1.*UNITS).*.[\r\n|\n]", re.MULTILINE), ""),             # Remove lines starting with '1 UNITS'
        (re.compile(r"\t+", re.MULTILINE), ","),                                # Replace tabs with commas
    ]

    with open(AnD_file, 'r', encoding='ISO-8859-1') as file:               # Load the data from the file
        for line in file:
            if not line.startswith("#"):                                        # Apply regex replacements
                for pattern, replacement in regex_patterns:
                    line = pattern.sub(replacement, line)
                if line:
                    AnD_data.append(line.strip())

    df = pd.DataFrame({'Data': AnD_data})                                       # Create a DataFrame from the extracted data
    df = df['Data'].str.split(',',expand=True)
    df.columns = df.iloc[0]                                                     # Adjust the headers of the data
    df = df[1:]
    df.reset_index(drop=True, inplace=True)

    return df                                                                   # Return the cleaned and formatted data 



""" Function to locate the headers of the file """
def locate_headers(AnD_data):
    headers = []
    for col in AnD_data.columns:                                               # Get the headers of the data
        headers.append(col)
    return headers                                                             # Return list of headers



""" Function time to minutes """
def convert_time(AnD_data):
    AnD_data["Test Time"] = pd.to_numeric(AnD_data["Test Time"]) / 60
    return AnD_data
