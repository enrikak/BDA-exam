
Closest Vessels Analysis Project

Project Overview:
This project analyzes AIS (Automatic Identification System) data to identify the two closest vessels to a specified center point (Latitude: 55.225000; Longitude: 14.245000
) of December 2021.

The process of finding two closest vessels:

Step 1: 
First script processes AIS data files to find the two closest vessels to the specified center point for each day of December 2021. The center point coordinates are given in task:
- Latitude: 55.225000
- Longitude: 14.245000

These daily closest vessels were saved as closest_vessels_[2021-12-day].csv files.

Step 2:
Second script then reads all the filtered daily CSV files and combines them into a single DataFrame. It identifies the two overall closest vessels from this combined data and saves the result in closest_overall_vessels.csv.

Step 3:
Third script reads the closest_overall_vessels.csv file and plots the 20-minute trajectories around the rendezvous moment for the two closest vessels. The plot shows their paths with respect to the center point.

Output:
MMSI's of two closest ships are: 219001468 and 304829000.

