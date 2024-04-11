import numpy as np
import scipy.stats
import librosa
import csv
import os
import argparse

def describe_freq(freqs):
    freqs_abs = np.abs(freqs)  # Convert to absolute values
    mean = np.mean(freqs_abs)
    std = np.std(freqs_abs) 
    maxv = np.amax(freqs_abs) 
    minv = np.amin(freqs_abs) 
    median = np.median(freqs_abs)
    skew = scipy.stats.skew(freqs_abs)
    kurt = scipy.stats.kurtosis(freqs_abs)
    q1 = np.quantile(freqs_abs, 0.25)
    q3 = np.quantile(freqs_abs, 0.75)
    mode = scipy.stats.mode(freqs_abs)[0]  # Corrected
    iqr = scipy.stats.iqr(freqs_abs)
    
    return [mean, std, maxv, minv, median, skew, kurt, q1, q3, mode, iqr]
    
def Energy(x):
    return np.sum(x**2)

def rmse(x):
    return np.sqrt(np.mean(x**2))
    
# Function to process each WAV file in the folder
def process_folder(folder_path, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Mean_Freq', 'Std_Freq', 'Max_Freq', 'Min_Freq', 'Median_Freq', 'Skew_Freq', 'Kurtosis_Freq', 'Q1_Freq', 'Q3_Freq', 'Mode_Freq', 'IQR_Freq',
                          'Energy', 'RMSE', 'Zero_Crossings'] )

        for filename in os.listdir(folder_path):
            if filename.endswith('.wav'):
                filepath = os.path.join(folder_path, filename)
                
                try:
                    # Load audio file
                    x, sr = librosa.load(filepath)
                    
                    # Check if the array is not empty
                    if x.size == 0:
                        print(f"Skipping {filename}: Empty audio file.")
                        continue
                    
                    # Calculate FFT frequencies
                    freqs = np.fft.fftfreq(x.size)
                    
                    # Describe frequency features
                    freq_features = describe_freq(freqs)
                    
                    # Calculate Energy and RMSE
                    energy = Energy(x)
                    rmse_val = rmse(x)
                    
                    # Calculate Zero Crossings
                    zero_crossings = sum(librosa.zero_crossings(x, pad=False))
                    
                    # Write features to CSV
                    writer.writerow([filename] + freq_features + [energy, rmse_val, zero_crossings] )
                    
                    print(f"Features written for {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Extract audio features from WAV files in a directory.')
parser.add_argument('--folder', type=str, help='Input folder containing WAV files')
parser.add_argument('--output', type=str, help='Output CSV file name')
args = parser.parse_args()

# Process folder and write features to CSV
process_folder(args.folder, args.output)

print("Features written to:", args.output)

