# v. 5.4.0 231111

import logging

from config_util import get_qqplot_params
from plot_util import common_axes_personalization, handle_subplot_err
from scipy.stats import probplot

def addplot_qq_sign(config, opdesc, orig_ylabel, targetAxes, signal):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_qq_raw(config, opdesc, orig_ylabel, targetAxes, signal)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_qq_raw(config, opdesc, orig_ylabel, target_ax, signal):
    logger = logging.getLogger(__name__)

    pbgcolor, plot_title_base, qq_type, orig_xlabel, def_ylabel, orig_grid, orig_yscale, comp_linewidth, comp_color, sign_color, marker, markerface_color, markersize, shape_param, scale_param = get_qqplot_params(config)
    plot_title = plot_title_base + ' (' + qq_type + ')'
    ylabel = orig_ylabel if (orig_ylabel) else def_ylabel
    
    # Create Q-Q plot
    probplot(signal, sparams=(shape_param, scale_param), dist=qq_type, plot=target_ax)
    signal_line = target_ax.get_lines()[0]
    signal_line.set_marker(marker)
    signal_line.set_markerfacecolor(markerface_color)
    signal_line.set_markersize(markersize)
    signal_line.set_color(sign_color)

    compare_line = target_ax.get_lines()[1]
    compare_line.set_linewidth(comp_linewidth)
    compare_line.set_color(comp_color)

    # Customize the plot (optional)
    common_axes_personalization(target_ax, plot_title, orig_xlabel, ylabel, orig_grid, orig_yscale, None, None, pbgcolor)
    #common_axes_personalization(phasepl_axes, ph_title, ph_xlabel, ph_ylabel, ph_grid_reqd, ph_yscale, ftphase_freq_limits, ftphase_val_limits, ph_bgcolor)
    
    #target_ax.plot(time, signal, color=orig_color, linewidth=orig_lwidth, label=orig_label)
    logger.debug('Subplot created (' + opdesc + ')')
