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


def main(input_path=None,
         output_path=None):

    energy_band_df = extract_energy_bands(input_path)
    plot_energy_band(df, outpath=os.path.join(output_path, "energy_band.html"))

    # Loudness
    loudness_df = extract_loudness(file)
    plot_loudness(loudness_df, outpath=os.path.join(output_path, "loudness.html"))


if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Analyze dj mix")
    parser.add_argument('-i', '--input_path',
                        default='data/test_frame.mp3',
                        help="Path of the audio files")
    parser.add_argument('-o', '--output_path',
                        default='output/',
                        help="Path where to store the data frame")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    main(
        input_path=args.input_path,
        output_path=args.output_path
    )
