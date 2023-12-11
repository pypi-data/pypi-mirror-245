# v. 8.5.0 231123

import logging
from config_util import get_ftplot_params
from plot_util import common_axes_personalization, add_plot_tooltip, handle_subplot_err

def addplot_ft(config, opdesc, targetAxes, frequencies, signal_fft_magnitude, frequency_grain, ft_freq_limits, ft_magn_limits, dc_offset_suppressed):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_ft_raw(config, opdesc, targetAxes, frequencies, signal_fft_magnitude, frequency_grain, ft_freq_limits, ft_magn_limits, dc_offset_suppressed)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_ft_raw(config, opdesc, ft_axes, frequencies, signal_fft_magnitude, frequency_grain, ft_freq_limits, ft_magn_limits, dc_offset_suppressed):
    logger = logging.getLogger(__name__)
    ft_bgcolor, ft_title, ft_xlabel, ft_ylabel, ft_yscale, ft_grid, ft_color, ft_linewidth = get_ftplot_params(config)
    ft_axes.plot(frequencies / frequency_grain, signal_fft_magnitude, color=ft_color, linewidth=ft_linewidth)
    common_axes_personalization(ft_axes, ft_title, ft_xlabel, ft_ylabel, ft_grid, ft_yscale, ft_freq_limits, ft_magn_limits, ft_bgcolor)
    add_plot_tooltip(config, ft_axes, [(dc_offset_suppressed, '-DC offset')])
    logger.debug('Subplot created (' + opdesc + ')')

