# v. 7.2.0 231117

import logging
from config_util import get_ftphaseplot_params
from plot_util import common_axes_personalization, handle_subplot_err

def addplot_ftphase(config, opdesc, targetAxes, frequencies, signal_ft_phase, frequency_grain, ftphase_freq_limits, ftphase_val_limits):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_ftphase_raw(config, opdesc, targetAxes, frequencies, signal_ft_phase, frequency_grain, ftphase_freq_limits, ftphase_val_limits)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_ftphase_raw(config, opdesc, phasepl_axes, frequencies, signal_ft_phase, frequency_grain, ftphase_freq_limits, ftphase_val_limits):
    logger = logging.getLogger(__name__)
    ph_title, ph_xlabel, ph_ylabel, ph_grid_reqd, ph_yscale, ph_color, ph_bgcolor, ph_linewid = get_ftphaseplot_params(config)
    #'Fourier Transform (Phase)', 'Frequency', 'Phase (radians)', True, 'linear', 'red', 'white'
    # Plot the phase
    phasepl_axes.plot(frequencies / frequency_grain, signal_ft_phase, color=ph_color, linewidth=ph_linewid)
    common_axes_personalization(phasepl_axes, ph_title, ph_xlabel, ph_ylabel, ph_grid_reqd, ph_yscale, ftphase_freq_limits, ftphase_val_limits, ph_bgcolor)
    logger.debug('Subplot created (' + opdesc + ')')
