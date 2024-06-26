import argparse
import glob
import numpy as np
import pandas as pd
import parselmouth
import os

from parselmouth.praat import call
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Function to measure voice pitch
def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    
    # Try to get the minimum pitch value
    try:
        pitch_floor = call(sound, "Get minimum pitch") # get the minimum pitch value from the sound file
    except parselmouth.PraatError:
        pitch_floor = f0min  # If the minimum pitch value cannot be obtained, use the provided value
    
    if f0min < pitch_floor:
        print(f"Warning: The provided minimum pitch value {f0min} is less than the minimum allowed pitch value {pitch_floor}. Adjusting minimum pitch value to {pitch_floor}.")
        f0min = pitch_floor  # Adjust the minimum pitch value if necessary
    
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) # create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    return meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer




# Function to run PCA
def runPCA(df):
    # Z-score the Jitter and Shimmer measurements
    features = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    # Separating out the features
    x = df.loc[:, features].values
    
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    x_imputed = imputer.fit_transform(x)
    
    # Standardizing the features
    x_scaled = StandardScaler().fit_transform(x_imputed)
    
    # PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x_scaled)
    principalDf = pd.DataFrame(data=principalComponents, columns=['JitterPCA', 'ShimmerPCA'])
    return principalDf
    
    

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Measure pitch of all WAV files in a directory.')
parser.add_argument('--folder', type=str, help='Input folder containing WAV files')
parser.add_argument('--output', type=str, help='Output CSV file name')
args = parser.parse_args()

# Folder containing the WAV files
input_folder = args.folder
# Output CSV file name
output_csv = args.output

# Create lists to store the results
file_list = []
mean_F0_list = []
sd_F0_list = []
hnr_list = []
localJitter_list = []
localabsoluteJitter_list = []
rapJitter_list = []
ppq5Jitter_list = []
ddpJitter_list = []
localShimmer_list = []
localdbShimmer_list = []
apq3Shimmer_list = []
aqpq5Shimmer_list = []
apq11Shimmer_list = []
ddaShimmer_list = []

# Go through all the wave files in the folder and measure pitch
for wave_file in glob.glob(os.path.join(input_folder, "*.wav")):
    try:
        (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(wave_file, 75, 500, "Hertz")
        file_list.append(wave_file) # make an ID list
        mean_F0_list.append(meanF0) # make a mean F0 list
        sd_F0_list.append(stdevF0) # make a sd F0 list
        hnr_list.append(hnr)
        localJitter_list.append(localJitter)
        localabsoluteJitter_list.append(localabsoluteJitter)
        rapJitter_list.append(rapJitter)
        ppq5Jitter_list.append(ppq5Jitter)
        ddpJitter_list.append(ddpJitter)
        localShimmer_list.append(localShimmer)
        localdbShimmer_list.append(localdbShimmer)
        apq3Shimmer_list.append(apq3Shimmer)
        aqpq5Shimmer_list.append(aqpq5Shimmer)
        apq11Shimmer_list.append(apq11Shimmer)
        ddaShimmer_list.append(ddaShimmer)
        print(f"Completed processing {os.path.basename(wave_file)}.")
    except parselmouth.PraatError as e:
        print(f"Error processing {os.path.basename(wave_file)}: {e}")
        continue  # Skip this file and continue with the next one


# Create a DataFrame to store the results
df = pd.DataFrame(np.column_stack([file_list, mean_F0_list, sd_F0_list, hnr_list, localJitter_list, localabsoluteJitter_list, rapJitter_list, ppq5Jitter_list, ddpJitter_list, localShimmer_list, localdbShimmer_list, apq3Shimmer_list, aqpq5Shimmer_list, apq11Shimmer_list, ddaShimmer_list]),
                               columns=['voiceID', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter', 
                                        'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 
                                        'apq11Shimmer', 'ddaShimmer'])

# Run PCA
pcaData = runPCA(df)
df = pd.concat([df, pcaData], axis=1)

# Write out the updated dataframe
df.to_csv(output_csv, index=False)

print("Jitter and Shimmer Features has been extracted")

