# v. 7.2.0 231117

import numpy as np

import logging
from config_util import get_wvletplot_params
from plot_util import common_axes_personalization, handle_subplot_err

import matplotlib.pyplot as plt

def addplot_wavelet(config, opdesc, targetAxes, orig_xlabel, time, wv_scales, wavelet_transform_data, wavelet_type):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_wavelet_raw(config, opdesc, targetAxes, orig_xlabel, time, wv_scales, wavelet_transform_data, wavelet_type)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_wavelet_raw(config, opdesc, wavel_axes, wv_xlabel, time, wv_scales, wavelet_transform_data, wavelet_type):
    logger = logging.getLogger(__name__)
    wv_aspect, wv_cmap, wv_interpolation, wv_origin, cbar_label, wvcbar_orientation, wv_title, wv_ylabel, wv_grid = get_wvletplot_params(config)
    # Plot the wavelet coefficients
    im = wavel_axes.imshow(wavelet_transform_data, aspect=wv_aspect, extent=[np.min(time), np.max(time), wv_scales[0], wv_scales[-1]],
       cmap=wv_cmap, interpolation=wv_interpolation, origin=wv_origin)
    #im = wavel_axes.imshow(wavelet_transform_data, aspect=wv_aspect, extent=[np.min(time), np.max(time), wv_scales[0], wv_scales[-1]],
    #   cmap=wv_cmap, interpolation=wv_interpolation, origin=wv_origin)
    # Set labels and title
    wv_title = wv_title + ('' if (wavelet_type is None) else ' (type: ' + wavelet_type + ')')
    common_axes_personalization(wavel_axes, wv_title, wv_xlabel, wv_ylabel, wv_grid, None, None, None, None)
    # Add a colorbar
    cbar = plt.colorbar(im, ax=wavel_axes, orientation=wvcbar_orientation)
    cbar.set_label(cbar_label)
    logger.debug('Subplot created (' + opdesc + ')')
