import pandas as pd
import matplotlib.pyplot as plt

# File containing the 2 closest vessels
filtered_csv_file_path = 'closest_overall_vessels.csv'

# This function calculates the 20-minute trajectory for a given vessel around the rendezvous moment.
def get_trajectory(df, mmsi, rendezvous_time):
    # Defining the start and end time for the 20-minute window
    start_time = rendezvous_time - pd.Timedelta(minutes=10)
    end_time = rendezvous_time + pd.Timedelta(minutes=10)

    # Returning the DataFrame filtered for the given MMSI and within the time window
    return df[(df['MMSI'] == mmsi) & (df['# Timestamp'] >= start_time) & (df['# Timestamp'] <= end_time)]

# Reading the filtered CSV file into a DataFrame
filtered_df = pd.read_csv(filtered_csv_file_path, parse_dates=['# Timestamp'])

# Checking if the DataFrame is not empty
if not filtered_df.empty:
    # Unique MMSI and names of the vessels
    vessels_info = filtered_df[['MMSI', 'Name']].drop_duplicates()

    # Initializing a plot for the trajectories
    plt.figure(figsize=(10, 6))

    # Looping through each unique MMSI
    for mmsi in vessels_info['MMSI']:
        # Finding the median timestamp for the current MMSI to use as the rendezvous time
        rendezvous_time = filtered_df[filtered_df['MMSI'] == mmsi]['# Timestamp'].median()

        # Getting the 20-minute trajectory around the rendezvous time
        trajectory_df = get_trajectory(filtered_df, mmsi, rendezvous_time)

        # Plotting the trajectory
        plt.plot(trajectory_df['Longitude'], trajectory_df['Latitude'], marker='o', label=f'MMSI: {mmsi}')

    # Plotting the center point
    plt.plot(14.245000, 55.225000, marker='x', color='red', markersize=10, label='Center')

    # Adding labels and legend to the plot
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('20-minute Trajectories of Closest Vessels')
    plt.legend()
    plt.grid()

    # Adjusting axis limits to focus on the area where points are close
    plt.xlim(14.244, 14.246)
    plt.ylim(55.224, 55.226)

    # Showing the plot
    plt.show()

    # Printing the MMSI and names of the vessels
    print("MMSI and Names of the Closest Vessels:")
    print(vessels_info.to_string(index=False))
else:
    # Printing a message if the DataFrame is empty
    print("The DataFrame is empty. No processing was done.")
