import os
import pandas as pd
from geopy.distance import geodesic

csv_directory = 'C:/Data/BDA/exam/aisdk-2021-12'

# Center coordinates that were provided in the task
center_latitude = 55.225000
center_longitude = 14.245000
center_coordinates = (center_latitude, center_longitude)

# This function reads a CSV file, then parses the timestamp column, and returns a DataFrame
# In case of an error an empty dataframe is returned
def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['# Timestamp'])
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# This function calculates the distance between the center coordinates and the vessel's coordinates for a given row
# In case of an error infinite distance is returned
def calculate_distance(row):
    """Function to calculate the distance of each vessel from the center."""
    try:
        vessel_coordinates = (row['Latitude'], row['Longitude'])
        return geodesic(center_coordinates, vessel_coordinates).kilometers
    except Exception as e:
        print(f"Error calculating distance for row {row}: {e}")
        return float('inf')  # Return an infinite distance in case of error

# List of CSV files in the directory (from december 1st to december 31st)
csv_files = [os.path.join(csv_directory, filename) for filename in os.listdir(csv_directory) if filename.endswith('.csv')]

# Iterating through each CSV file in the directory
for csv_file_path in csv_files:
    # Reading the CSV file
    df = read_csv_file(csv_file_path)

    if not df.empty:
        # Filtering out rows with invalid latitude or longitude (noise)
        valid_latitude = (df['Latitude'] >= -90) & (df['Latitude'] <= 90)
        valid_longitude = (df['Longitude'] >= -180) & (df['Longitude'] <= 180)
        df = df[valid_latitude & valid_longitude]

        # Calculating distance for each row
        df['distance'] = df.apply(calculate_distance, axis=1)

        # Filtering vessels within a 50 km radius
        filtered_df = df[df['distance'] <= 50]

        # Removing duplicates
        filtered_df = filtered_df.drop_duplicates(subset=['MMSI', '# Timestamp'])

        # Sorting by distance and select the 2 closest vessels
        closest_vessels_df = filtered_df.sort_values(by='distance').groupby('MMSI').first().nsmallest(2, 'distance').reset_index()

        # Saving the filtered DataFrame of the 2 closest vessels to a new CSV file
        output_file_name = f"closest_vessels_{os.path.basename(csv_file_path)}"
        closest_vessels_df.to_csv(output_file_name, index=False)

        print(f'Dataset of the 2 closest vessels for {csv_file_path} saved as {output_file_name}')
    else:
        print(f"The DataFrame for {csv_file_path} is empty. No processing was done.")
