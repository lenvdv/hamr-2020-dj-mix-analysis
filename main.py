import argparse
import essentia
import librosa
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

from essentia.standard import *
from essentia.streaming import *  # Use streaming mode to deal with long files (mixes)
from pylab import plot, show, figure, imshow
from scipy.signal import savgol_filter
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from src.feature_extraction import extract_loudness,extract_energy_bands, extract_spectral_complexity
from src.visualization import plot_energy_band, plot_loudness, plot_spectral_comp


def process_file_OLD(input_path=None, output_path=None):

    file = input_path
    sample_rate = librosa.get_samplerate(file)
    logging.info(f'Starting analysis of {file}')

    # ================================================
    # Declare audio loading stream and related parameters
    # ================================================

    frame_length = sample_rate * 60
    hop_length = sample_rate * 5
    block_length = 5 * 4
    # Load the audio as a stream
    stream = librosa.stream(file,
                            block_length=block_length,
                            frame_length=frame_length,
                            hop_length=hop_length,
                            )
    logging.info(f'Sample rate: {sample_rate}')

    # ================================================
    # Define features to extract
    # ================================================

    energy_band_params = [
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 20, 'stopCutoffFrequency' : 100},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 100, 'stopCutoffFrequency' : 200},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 200, 'stopCutoffFrequency' : 800},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 800, 'stopCutoffFrequency' : 2000},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 2000, 'stopCutoffFrequency' : 5000},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 5000, 'stopCutoffFrequency' : 8000},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 8000, 'stopCutoffFrequency' : 22050},
    ]

    def hz_to_bin(f, n_bins, sr):
        return int(np.round((f / sr) * n_bins))

    class EnergyBandSelf:

        ''' Feature extraction class that extracts the energy in a frequency band, given a power STFT spectrogram.'''

        def __init__(self, sampleRate=44100, startCutoffFrequency=20.0, stopCutoffFrequency=11025.0):
            self.sr = sampleRate
            self.f_start = startCutoffFrequency
            self.f_stop = stopCutoffFrequency

        def __call__(self, S_power):
            n_bins = S_power.shape[0]
            n_start, n_stop = hz_to_bin(self.f_start, n_bins, self.sr), hz_to_bin(self.f_stop, n_bins, self.sr)
            return np.sum(S_power[n_start:n_stop, :])
            # return np.median(np.sum(S_power[n_start:n_stop, :], axis=0))

    energy_band_extractors = [
        EnergyBandSelf(**kwargs) for kwargs in energy_band_params
    ]

    # ================================================
    # Feature extraction
    # ================================================
    energy_band_features = []

    # Read the librosa docs to understand how the blocks and frames relate to each other:
    # https://librosa.org/blog/2019/07/29/stream-processing/#Blocks
    for i, y_block in enumerate(stream):
        for j, n_start in enumerate(range(0,len(y_block), hop_length)):
            if j == 0 and i % 5 == 0:
                t = (j * hop_length + i * block_length * hop_length)/(60*sample_rate)
                print(
                    f'Processing from minute {t:.0f}.')
                logging.info(
                    f'Processing from minute {t:.0f}.')
            # Select the current audio frame
            y_frame = y_block[..., n_start:n_start+hop_length]
            # Calculate the STFT power spectrogram for this audio frame
            S = np.abs(librosa.stft(y_frame))**2
            # Calculate the energy in each of the predefined energy bands
            energy_band_features.append([e(S) for e in energy_band_extractors])
    # Back to a numpy array
    energy_band_features = np.array(energy_band_features)

    # ================================================
    # Plotting
    # ================================================

    toplot = energy_band_features / np.max(energy_band_features, axis=0)[np.newaxis, :]
    toplot = toplot / np.sum(toplot, axis=1)[:, np.newaxis]
    yhat = savgol_filter(toplot, 15, 3, axis=0)  # smooth the output a bit

    df = pd.DataFrame(data=toplot)

    return plot_data(df, output_path)



def plot_data(df,
              output_path,
              colorscale=px.colors.sequential.Cividis_r):

    print("Plotting the features....")
    fig = go.Figure()
    for i, (key, descr) in enumerate(df.iteritems()):
        fig.add_trace(go.Scatter(
            x=df.index, y=descr,
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5, color=colorscale[i]),
            stackgroup='one', # define stack group,
            name="Energy Band Level {}".format(i)
        ))


    fig.update_layout(yaxis_range=(0, 1))

    with open (output_path, 'w') as f:
        f.write(fig.to_html(full_html=False))
    print("Done! Result saved into file {}".format(output_path))

    return output_path

def process_file(input_path=None,
         output_path=None,
         output_csv=None):
    file_prefix = input_path.split(".wav")[0]
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    # 
    # spectral_complexity_df = extract_spectral_complexity(input_path)
    # plot_spectral_comp(spectral_complexity_df, outpath=os.path.join(output_path, "spectral_comp.html"))

    energy_band_df = extract_energy_bands(input_path)
    plot_energy_band(energy_band_df, outpath=os.path.join(output_path, "energy_band.html"))
    #
    # # Loudness
    # loudness_df = extract_loudness(input_path)
    # plot_loudness(loudness_df, outpath=os.path.join(output_path, "loudness.html"))


if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Analyze dj mix")
    parser.add_argument('-i', '--input_path',
                        default='data/test_frame.mp3',
                        help="Path of the audio files")
    parser.add_argument('-o', '--output_path',
                        default='output/',
                        help="Path where to store the data frame")
    parser.add_argument('-csv', '--output-csv',
                        default='output/csv/',
                        help="Where to save the csvs containing descriptors"
                        )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    process_file(
        input_path=args.input_path,
        output_path=args.output_path,
        output_csv=args.output_csv
    )
