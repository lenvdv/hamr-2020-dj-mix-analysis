import argparse
import essentia
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

    audio_files = os.listdir(input_path)
    file = os.path.join(input_path, audio_files[0])
    sample_rate = 44100
    logging.info(f'Starting analysis of {file}')

    # Loading
    t0 = time.time()
    # Load the audio in mono
    loader = essentia.streaming.MonoLoader(filename=file)
    # Framecutter
    frame_cutter = essentia.streaming.FrameCutter(frameSize=44100 * 30, hopSize=44100 * 60)
    w = essentia.streaming.Windowing(type='hann')
    # Estimate danceability
    danceability = essentia.standard.Danceability()
    # Outputs
    pool = essentia.Pool()

    # Connect everything
    loader.audio >> frame_cutter.signal
    frame_cutter.frame >> w.frame >> (pool, 'frames')

    #>> danceability.signal
    # danceability.danceability >> (pool, 'danceability')

    logging.info('Connected everything, starting the processing!')
    essentia.run(loader)

    print(len(pool['frames']))

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
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    main(
        input_path=args.input_path,
        output_path=args.output_path
    )
