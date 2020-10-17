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
    energy_band_params = [
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 20, 'stopCutoffFrequency' : 200},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 200, 'stopCutoffFrequency' : 1000},
        {'sampleRate' : sample_rate, 'startCutoffFrequency' : 1000, 'stopCutoffFrequency' : 2000},
    ]
    energy_band_extractors = [
        essentia.standard.EnergyBand(**kwargs) for kwargs in energy_band_params
    ]

    danceability = []
    energy_band_features = []
    for i, y_block in enumerate(stream):
        logging.debug(f'Processing block {i}')
        # danceability.append(danceability_extractor(y_block)[0])
        S = librosa.stft(y_block)
        spectrum_avg = np.aveg
    danceability = np.array(danceability)
    logging.info(f'Danceability: {danceability.shape}')

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


    timestamps = np.arange(frame.shape[0]) / 44100
    plot(timestamps, frame)

    plt.title("This is how the first 60 seconds of this audio looks like:")
    plt.xlabel("Time")
    show() # unnecessary if you started "ipython --pylab"


if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Analyze dj mix")
    parser.add_argument('-i', '--input_path',
                        help="Path of the audio files")
    parser.add_argument('-o', '--output_path',
                        help="Path where to store the data frame")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    main(
        input_path=args.input_path,
        output_path=args.output_path
    )
