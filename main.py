import essentia
from essentia.standard import *
import os
import sys
import time
import numpy as np
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt
import argparse


def main(input_path=None,
         output_path=None):
    data_path = "data"
    audio_files = os.listdir("data")
    file = os.path.join(data_path, audio_files[0])
    sample_rate = 44100

    # Loading
    t0 = time.time()
    # we start by instantiating the audio loader:
    loader = essentia.standard.MonoLoader(filename=file)

    # and then we actually perform the loading:
    audio = loader()

    print("Audio loaded, time elapsed: {} ".format(time.time() - t0))
    print("Duration of the audio file {} minutes".format(audio.shape[0] / (sample_rate * 60)))


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

    main(
        input_path=args.input_path,
        output_path=args.output_path
    )
