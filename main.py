import argparse
import essentia
import librosa
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from essentia.standard import *
from essentia.streaming import *  # Use streaming mode to deal with long files (mixes)
from pylab import plot, show, figure, imshow

def main(input_path=None,
         output_path=None):

    file = input_path
    sample_rate = librosa.get_samplerate(file)
    logging.info(f'Starting analysis of {file}')

    # Declare audio loading stream
    stream = librosa.stream(file,
                            block_length=1,
                            frame_length=sample_rate * 20,
                            hop_length=sample_rate*10
                            )
    logging.info(f'Sample rate: {sample_rate}')
    # Load the audio as a stream
    danceability_extractor = essentia.standard.Danceability()
    danceability = []
    for i, y_block in enumerate(stream):
        logging.debug(f'Processing block {i}')
        danceability.append(danceability_extractor(y_block)[0])
    danceability = np.array(danceability)
    logging.info(f'Danceability: {danceability.shape}')

    result_df = pd.DataFrame()

    result_df['danceability'] = danceability





    import ipdb; ipdb.set_trace()
    plt.figure()
    plt.plot(danceability)
    plt.show()

def extract_desciptors(audio,
                       frame_size = 44100 * 60,
                       descriptors = ['lowlevel.average_loudness', 'tonal.tuning_frequency', 'lowlevel.dissonance.mean']):
    # 1 Mn frames
    musex = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])

    frame_size = sample_rate * 1024
    frame_gen = FrameGenerator(audio, frameSize=frame_size, hopSize=512, startFromZero=True)
    frame_path = 'data/tmp.mp3'
    writer = MonoWriter(filename=frame_path)

    result = pd.DataFrame(index = np.arange(frame_gen.num_frames()), columns = descriptors)

    for i, frame in enumerate(frame_gen):

        writer(frame)
        features, features_frames = musex(frame_path)
        for descr in descriptors:
            result.loc[i, descr] = features[descr]



def plot_audio(frame):
    frame = frame_gen.next()
    # pylab contains the plot() function, as well as figure, etc... (same names as Matlab)

    plt.rcParams['figure.figsize'] = (15, 6) # set plot sizes to something larger than default

    # Read the librosa docs to understand how the blocks and frames relate to each other:
    # https://librosa.org/blog/2019/07/29/stream-processing/#Blocks
    for i, y_block in enumerate(stream):
        for j, n_start in enumerate(range(0,len(y_block), hop_length)):
            if j == 0 and i % 5 == 0:
                logging.info(
                    f'Processing from minute {(j * hop_length + i * block_length * hop_length)/(60*sample_rate)}.')
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
    yhat = savgol_filter(toplot, 15, 3, axis=0)  # smooth the output a bit

    #
    # plt.figure()
    # plt.plot(yhat)
    # # plt.plot(toplot, linestyle=':')
    # plt.show()


    # ===================================================
    # Pandas dataframe
    #================================================



if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Analyze dj mix")
    parser.add_argument('-i', '--input_path',
                        default='data/test_frame.mp3',
                        help="Path of the audio files")
    parser.add_argument('-o', '--output_path',
                        default='data/output.csv',
                        help="Path where to store the data frame")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    main(
        input_path=args.input_path,
        output_path=args.output_path
    )
