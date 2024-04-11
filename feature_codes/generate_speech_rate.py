import os
import librosa
import csv
import argparse

def extract_sample_rates(folder_path, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Sample Rate'])

        for filename in os.listdir(folder_path):
            if filename.endswith('.wav'):
                filepath = os.path.join(folder_path, filename)
                try:
                    audio_data, sample_rate = librosa.load(filepath, sr=None)
                    writer.writerow([filename, sample_rate])
                    print(f"Sample rate extracted for {filename}: {sample_rate}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Extract sample rates of WAV files in a directory.')
parser.add_argument('--folder', type=str, help='Input folder containing WAV files')
parser.add_argument('--output', type=str, help='Output CSV file name')
args = parser.parse_args()

# Extract sample rates and write to CSV
if args.folder and args.output:
    extract_sample_rates(args.folder, args.output)
    print("Sample rates written to:", args.output)
else:
    print("Please provide both input folder path and output CSV file name.")

