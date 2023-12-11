# v. 8.2.0 231121

import numpy as np
from scipy.signal import spectrogram

import logging
from config_util import get_3dspectrogramplot_params
from plot_util import common_axes_personalization, handle_subplot_err

def addplot_3d_spectrogram(config, opdesc, targetAxes, orig_xlabel, sampling_freq, time, signal):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_3dspectrogram_raw(config, opdesc, targetAxes, orig_xlabel, sampling_freq, time, signal)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_3dspectrogram_raw(config, opdesc, spec3d_axes, spec_xlabel, sampling_freq, time, signal):
    logger = logging.getLogger(__name__)
    plot_title, db_multiplier, ylabel, zlabel, color_map, edge_colors, bgcolor = get_3dspectrogramplot_params(config)

    # Calculate spectrogram
    frequencies, times, Sxx = spectrogram(signal, sampling_freq)
    # Create a matplotlib figure
    #fig, spec3d_axes = plt.subplots(subplot_kw={'projection': '3d'})

    # Set the 3D projection on the existing spec3d_axes object
    #spec3d_axes.view_init(elev=25, azim=-55)
    #spec3d_axes.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
    times_mesh, frequencies_mesh = np.meshgrid(times, frequencies)
    spec3d_axes.plot_surface(times_mesh, frequencies_mesh, db_multiplier * np.log10(Sxx), cmap=color_map, edgecolors=edge_colors)
    # Add labels and title

    common_axes_personalization(spec3d_axes, plot_title, spec_xlabel, ylabel, None, None, None, None, bgcolor)
    #spec3d_axes.set_xlabel(spec_xlabel)
    #spec3d_axes.set_ylabel(ylabel)
    #spec3d_axes.set_title(plot_title)
    spec3d_axes.set_zlabel(zlabel)
    logger.debug('Subplot created (' + opdesc + ')')
