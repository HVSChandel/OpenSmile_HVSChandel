import os
import opensmile
import argparse

# Initialize ArgumentParser
parser = argparse.ArgumentParser(description='Process WAV files and extract GeMAPS features.')

# Add argument for the input directory containing WAV files
parser.add_argument('--input_dir', type=str, help='Input directory containing WAV files')

# Parse the arguments
args = parser.parse_args()

# Retrieve the input directory path from the arguments
input_dir = args.input_dir

# Create a subfolder named "Gemaps" to store output CSV files
output_dir = os.path.join(input_dir, "Gemaps")
os.makedirs(output_dir, exist_ok=True)

# Initialize opensmile Smile object
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

# Loop through all WAV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".wav"):
        # Define input and output file paths
        input_wav = os.path.join(input_dir, filename)
        output_csv = os.path.join(output_dir, filename.replace(".wav", ".csv"))

        # Process the input WAV file
        result_df = smile.process_file(input_wav)

        # Now use only the three center formant frequencies
        center_formant_freqs = ['F1frequency_sma3nz', 'F2frequency_sma3nz', 'F3frequency_sma3nz']
        formant_df = result_df[center_formant_freqs]

        # Add filename column to the DataFrame
        formant_df['filename'] = filename

        # Reorder columns to have 'filename' as the first column
        formant_df = formant_df[['filename'] + center_formant_freqs]

        # Save the results to a CSV file with the same name as the WAV file
        formant_df.to_csv(output_csv, index=False)

        # Print completion message
        print(f"Processed {filename} and saved results to {output_csv}")

print("Output CSV files saved successfully in the 'Gemaps' folder.")

