import os
import argparse
import numpy as np
import librosa
import csv

# Function to load the WAV file
def load_wav_file(file_path):
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    return audio_data, sample_rate

# Function to extract LPC features
def extract_lpc_features(audio_data, sample_rate, order=12):
    # Calculate LPC coefficients using scipy
    lpc_coeffs = librosa.lpc(audio_data, order=order)
    return lpc_coeffs

# Function to process all WAV files in a folder and extract LPC features
def process_wav_folder(folder_path, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'LPC Coefficients'])

        for filename in os.listdir(folder_path):
            if filename.endswith('.wav'):
                filepath = os.path.join(folder_path, filename)
                audio_data, sample_rate = load_wav_file(filepath)
                lpc_features = extract_lpc_features(audio_data, sample_rate)
                writer.writerow([filename, lpc_features])
                print("LPC features extracted for:", filename)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Extract LPC features from WAV files in a folder.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing WAV files.")
    parser.add_argument("output_csv", type=str, help="Output CSV file to save LPC features.")
    args = parser.parse_args()

    folder_path = args.folder_path
    output_csv = args.output_csv
    process_wav_folder(folder_path, output_csv)
    print("LPC features extraction completed. Results saved to:", output_csv)

if __name__ == "__main__":
    main()

