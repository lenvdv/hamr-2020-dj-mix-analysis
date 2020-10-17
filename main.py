import argparse
import essentia
import librosa
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

from src.feature_extraction import extract_loudness,extract_energy_bands, extract_spectral_complexity
from src.visualization import plot_energy_band, plot_loudness, plot_spectral_comp


def process_file(
        input_path=None,
        output_path=None,
        output_csv=None):
    file_prefix = input_path.split(".wav")[0]
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    spectral_complexity_df = extract_spectral_complexity(input_path)
    output_file = os.path.join(output_path, "spectral_comp.html")
    plot_spectral_comp(spectral_complexity_df, outpath=output_file)

    energy_band_df = extract_energy_bands(input_path)
    output_file = os.path.join(output_path, "energy_band.html")
    plot_energy_band(energy_band_df, outpath=output_file)

    #
    # # Loudness
    # loudness_df = extract_loudness(input_path)
    # plot_loudness(loudness_df, outpath=os.path.join(output_path, "loudness.html"))

    return output_file


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
