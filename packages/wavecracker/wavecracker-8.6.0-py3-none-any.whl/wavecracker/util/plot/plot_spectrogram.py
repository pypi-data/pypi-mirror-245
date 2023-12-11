# v. 7.2.0 231117

import numpy as np

import logging
from config_util import get_spectrogramplot_params
from plot_util import common_axes_personalization, handle_subplot_err

def addplot_spectrogram(config, opdesc, targetAxes, orig_xlabel, sampling_freq, time, signal):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_spectrogram_raw(config, opdesc, targetAxes, orig_xlabel, sampling_freq, time, signal)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_spectrogram_raw(config, opdesc, spec_axes, spec_xlabel, sampling_freq, time, signal):
    logger = logging.getLogger(__name__)
    # Plot the spectrogram with consistent time values
    spec_title, spec_ylabel, spec_colorbar_label, spec_yscale, spec_grid, spec_color_map = get_spectrogramplot_params(config)
    #spec_freq_grain = 1000
    spec, _, _, _ = spec_axes.specgram(signal, Fs=sampling_freq, cmap=spec_color_map)
    # Manually create the spectrogram using pcolormesh
    extent = (time.min(), time.max(), 0, sampling_freq / 2)
    pcm = spec_axes.pcolormesh(np.linspace(extent[0], extent[1], spec.shape[1]), np.linspace(extent[2], extent[3], spec.shape[0]), 10 * np.log10(spec), cmap=spec_color_map)
    common_axes_personalization(spec_axes, spec_title, spec_xlabel, spec_ylabel, spec_grid, spec_yscale, None, None, None)
    # Add colorbar for the spectrogram

    cbar = spec_axes.figure.colorbar(pcm, ax=spec_axes)
    #cbar = fig.colorbar(pcm, ax=spec_axes)

    cbar.set_label(spec_colorbar_label)
    logger.debug('Subplot created (' + opdesc + ')')
