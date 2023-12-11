# v. 8.5.0 231123

import logging
from config_util import get_psdplot_params
from plot_util import common_axes_personalization, add_plot_tooltip, handle_subplot_err

def addplot_psd(config, opdesc, targetAxes, psd_x_vals, psd_y_vals, frequency_grain, psd_freq_limits, psd_pow_limits, dc_offset_suppressed):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_psd_raw(config, opdesc, targetAxes, psd_x_vals, psd_y_vals, frequency_grain, psd_freq_limits, psd_pow_limits, dc_offset_suppressed)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_psd_raw(config, opdesc, psd_axes, psd_x_vals, psd_y_vals, frequency_grain, psd_freq_limits, psd_pow_limits, dc_offset_suppressed):
    logger = logging.getLogger(__name__)
    psd_title, psd_xlabel, psd_ylabel, psd_grid_reqd, psd_yscale, psd_color, psd_bgcolor, psd_linewid = get_psdplot_params(config)
    psd_axes.plot(psd_x_vals / frequency_grain, psd_y_vals, color=psd_color, linewidth=psd_linewid)
    common_axes_personalization(psd_axes, psd_title, psd_xlabel, psd_ylabel, psd_grid_reqd, psd_yscale, psd_freq_limits, psd_pow_limits, psd_bgcolor)
    add_plot_tooltip(config, psd_axes, [(dc_offset_suppressed, '-DC offset')])
    logger.debug('Subplot created (' + opdesc + ')')
