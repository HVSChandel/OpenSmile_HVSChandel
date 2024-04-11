import pandas as pd
import os

# Directory containing the CSV files
csv_directory = "/home/hvs/hvschandel/multiclass_speech_disorder/final-speech-disorder/Word-Repetition/Gemaps"

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

# Initialize an empty DataFrame to store merged data
merged_data = pd.DataFrame()

# Loop through each CSV file and merge data
for csv_file in csv_files:
    csv_path = os.path.join(csv_directory, csv_file)
    
    try:
        # Read the CSV file
        data = pd.read_csv(csv_path, header=None)
        
        # Check if the file is empty (no columns to parse)
        if data.empty:
            print(f"Empty file found: {csv_file}. Deleting it.")
            os.remove(csv_path)
            continue
        
        # Use the first row as column names
        data.columns = data.iloc[0]
        
        # Skip the first row (column names) and append the rest to the merged data
        merged_data = merged_data.append(data.iloc[1:], ignore_index=True)
    
    except pd.errors.EmptyDataError:
        print(f"EmptyDataError for file: {csv_file}. Deleting it.")
        os.remove(csv_path)

# Save the merged data to a new CSV file
merged_data.to_csv("/home/hvs/hvschandel/multiclass_speech_disorder/final-speech-disorder/Word-Repetition_formant_features.csv", index=False)

