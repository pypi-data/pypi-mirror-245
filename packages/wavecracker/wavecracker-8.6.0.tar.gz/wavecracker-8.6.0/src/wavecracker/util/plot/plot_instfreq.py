# v. 8.6.0 231210

import logging
from config_util import get_instfreqplot_params
from plot_util import common_axes_personalization, handle_subplot_err

def addplot_instfreq(config, opdesc, orig_xlabel, orig_ylabel, targetAxes, time, signal, inst_freq, sig_time_window, sig_ampl_limits):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_instfreq_raw(config, opdesc, orig_xlabel, orig_ylabel, targetAxes, time, signal, inst_freq, sig_time_window, sig_ampl_limits)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')


def addplot_instfreq_raw(config, opdesc, orig_xlabel, orig_ylabel, target_ax, time, signal, inst_freq, sig_time_window, sig_ampl_limits):
    logger = logging.getLogger(__name__)
    plot_title, ylabel, orig_bgcolor, orig_yscale, orig_grid, sig_color, ifcolor, orig_lwidth, sig_linestyle, sig_linewidth, sig_ylabel = get_instfreqplot_params(config)
    #target_ax.plot(time[:-1], inst_freq, linestyle=sig_linestyle, color=sig_color, linewidth=sig_linewidth, label=orig_label)
    #target_ax.plot(time, signal, linestyle=sig_linestyle, color=sig_color, linewidth=sig_linewidth, label='orig2')
    target_ax.plot(time, signal, linestyle=sig_linestyle, color=sig_color, linewidth=sig_linewidth)

    ax2 = target_ax.twinx()
    ax2.plot(time[:-1], inst_freq, linewidth=orig_lwidth, color=ifcolor)
    #ax2.plot(time[:-1], inst_freq, label='Instantaneous Frequency', color='red')
    ax2.set_ylabel(ylabel, color=ifcolor)

    common_axes_personalization(target_ax, plot_title, orig_xlabel, sig_ylabel, orig_grid, orig_yscale, sig_time_window, sig_ampl_limits, orig_bgcolor)

    logger.debug('Subplot created (' + opdesc + ')')
