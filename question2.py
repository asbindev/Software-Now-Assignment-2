# question2.py
import pandas as pd
import glob
import os

# Define Australian seasons and the months that belong to each season
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

# Order of months in CSV files
MONTH_ORDER = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

def load_data():
    """
    Load all CSV files from the 'temperatures' folder.
    Convert from wide (months as columns) to long format:
    Station | Month | Temperature
    """
    # Find all CSV files matching pattern
    files = glob.glob(os.path.join("temperatures", "stations_group_*.csv"))
    if not files:
        print("No CSV files found in the 'temperatures' folder.")
        return pd.DataFrame()

    df_list = []
    for f in files:
        try:
            df_temp = pd.read_csv(f)
            # Ensure required columns exist
            required_cols = ["STATION_NAME"] + MONTH_ORDER
            if not all(col in df_temp.columns for col in required_cols):
                print(f"Skipping {f}: Missing required columns.")
                continue

            # Reshape from wide to long format for easier processing
            df_long = df_temp.melt(
                id_vars=["STATION_NAME"],  # Keep Station Name
                value_vars=MONTH_ORDER,    # Columns to unpivot
                var_name="Month",          # New column for month names
                value_name="Temperature"   # New column for temperature values
            )
            df_list.append(df_long)
        except Exception as e:
            print(f"Error reading {f}: {e}")
    
    # Combine all CSVs into one DataFrame
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        print("No valid CSV data to process.")
        return pd.DataFrame()

def seasonal_average(df):
    """
    Calculate average temperature for each Australian season across all stations.
    Save the results to 'average_temp.txt'.
    """
    try:
        results = {}
        for season, months in SEASONS.items():
            # Calculate mean temperature for the months in this season
            avg = df[df['Month'].isin(months)]['Temperature'].mean(skipna=True)
            results[season] = avg if pd.notna(avg) else float('nan')
        
        # Write results to file
        with open("average_temp.txt", "w") as f:
            for s, v in results.items():
                f.write(f"{s}: {v:.1f}°C\n")
        print("Seasonal averages saved to average_temp.txt")
    except Exception as e:
        print(f"Error calculating seasonal averages: {e}")

def largest_temp_range(df):
    """
    Find station(s) with the largest temperature range (max - min).
    Save the results to 'largest_temp_range_station.txt'.
    """
    try:
        grouped = df.groupby("STATION_NAME")["Temperature"]
        ranges = grouped.max() - grouped.min()  # Calculate range for each station
        max_range = ranges.max()               # Find the largest range
        stations = ranges[ranges == max_range] # Find all stations with this range
        
        # Write results to file
        with open("largest_temp_range_station.txt", "w") as f:
            for station in stations.index:
                mx = grouped.max()[station]
                mn = grouped.min()[station]
                f.write(f"{station}: Range {mx-mn:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)\n")
        print("Largest temperature range saved to largest_temp_range_station.txt")
    except Exception as e:
        print(f"Error calculating largest temperature range: {e}")

def temperature_stability(df):
    """
    Find the most stable (smallest std dev) and most variable (largest std dev) stations.
    Save the results to 'temperature_stability_stations.txt'.
    """
    try:
        grouped = df.groupby("STATION_NAME")["Temperature"]
        stds = grouped.std()  # Standard deviation for each station
        if stds.empty:
            print("No temperature data to calculate stability.")
            return

        # Identify stations with min and max standard deviation
        most_stable = stds[stds == stds.min()]
        most_variable = stds[stds == stds.max()]
        
        # Write results to file
        with open("temperature_stability_stations.txt", "w") as f:
            for st in most_stable.index:
                f.write(f"Most Stable: {st}: StdDev {most_stable[st]:.1f}°C\n")
            for st in most_variable.index:
                f.write(f"Most Variable: {st}: StdDev {most_variable[st]:.1f}°C\n")
        print("Temperature stability saved to temperature_stability_stations.txt")
    except Exception as e:
        print(f"Error calculating temperature stability: {e}")

if __name__ == "__main__":
    try:
        # Load and preprocess data
        df = load_data()
        if df.empty:
            print("No data to process. Exiting program.")
        else:
            # Drop rows with missing temperature values
            df = df.dropna(subset=["Temperature"])
            
            # Perform all analyses
            seasonal_average(df)
            largest_temp_range(df)
            temperature_stability(df)
            print("All results saved successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
