import os
import pandas as pd

# Function to process a CSV file
def process_csv(csv_path):
    try:
        # Read the CSV file with column names and data separated by semicolons
        data = pd.read_csv(csv_path, sep=',', skiprows=1, header=None)
        
        # Get the column names from the first row
        column_names = pd.read_csv(csv_path, sep=',', nrows=0).columns.tolist()
        
        # Assign column names to the DataFrame
        data.columns = column_names
        
        # Calculate the mean of each column
        column_means = data.mean(axis=0)
        
        # Create a DataFrame with mean values
        mean_data = pd.DataFrame([column_means], columns=column_names)
        
        # Update the CSV file with mean values
        mean_data.to_csv(csv_path, index=False)
        
        print(f"Processed {csv_path}")
    except pd.errors.EmptyDataError:
        # Handle the EmptyDataError by removing the file
        os.remove(csv_path)
        print(f"Error: Removed empty file {csv_path}")

# Folder containing the CSV files
folder_path = "/home/hvs/hvschandel/multiclass_speech_disorder/final-speech-disorder/Word-Repetition/Gemaps"  # Replace with the folder path

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# Loop through each CSV file and update mean data
for csv_file in csv_files:
    csv_path = os.path.join(folder_path, csv_file)
    process_csv(csv_path)

print("Mean values updated in all CSV files.")

