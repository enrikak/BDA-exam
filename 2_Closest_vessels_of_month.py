import os
import pandas as pd
from geopy.distance import geodesic

filtered_csv_directory = os.getcwd()

# This function reads all filtered CSV files and concatenates them into a single DataFrame.
def read_filtered_csv_files(directory):
    # Listing all filtered files in the directory that start with 'closest_vessels_' and end with '.csv'
    all_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if
                 filename.startswith('closest_vessels_') and filename.endswith('.csv')]

    df_list = []

    # Looping through each day file and read it into a DataFrame
    for file in all_files:
        try:
            # Reading the CSV file, parsing the '# Timestamp' column as datetime
            df = pd.read_csv(file, parse_dates=['# Timestamp'])
            df_list.append(df)
        except Exception as e:
            # Print an error message if the file cannot be read
            print(f"Error reading {file}: {e}")

    # Concatenating all DataFrames if the list is not empty
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        return combined_df
    else:
        # If no files were read an empty dataframe is returned
        return pd.DataFrame()


# Reading all filtered CSV files
combined_df = read_filtered_csv_files(filtered_csv_directory)

if not combined_df.empty:
    # Sorting the combined DataFrame by distance
    # Grouping by 'MMSI' and taking the first occurrence of each group
    # Selecting the 2 closest vessels based on the smallest distance
    closest_overall_vessels_df = combined_df.sort_values(by='distance').groupby('MMSI').first().nsmallest(2,
                                                                                                          'distance').reset_index()

    # Saving the DataFrame of the 2 closest vessels to a new CSV file
    output_file_name = 'closest_overall_vessels.csv'
    closest_overall_vessels_df.to_csv(output_file_name, index=False)

    print(f'Dataset of the 2 closest vessels overall saved as {output_file_name}')
else:
    print("The combined DataFrame is empty. No processing was done.")
