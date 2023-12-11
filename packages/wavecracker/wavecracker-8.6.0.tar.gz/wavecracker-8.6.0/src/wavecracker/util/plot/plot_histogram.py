# v. 7.2.0 231117

import logging
from config_util import get_histplot_params
from plot_util import common_axes_personalization_raw, handle_subplot_err
import random

def addplot_histogram(config, opdesc, targetAxes, signal, hist_val_limits, hist_freq_limits, rainbow_colors):
    logger = logging.getLogger(__name__)
    if (not (targetAxes is None)):
        try:
            addplot_histogram_raw(config, opdesc, targetAxes, signal, hist_val_limits, hist_freq_limits, rainbow_colors)
        except Exception as pe:
            err_msg = str(pe)
            handle_subplot_err(config, targetAxes, opdesc, err_msg)
    else:
        logger.warning('PLOT SKIPPED, no more room (' + opdesc + ')')        

def addplot_histogram_raw(config, opdesc, hist_axes, signal, hist_val_limits, hist_freq_limits, rainbow_colors):
    logger = logging.getLogger(__name__)
    hist_title, orighist_xlabel, orighist_ylabel, hist_grid_reqd, hist_valscale, bins_set, density_set, hist_edgecolor, hist_bgcolor, hist_lwidth, is_horiz = get_histplot_params(config)

    hist_orient = 'vertical'
    hist_xlabel = orighist_xlabel
    hist_ylabel = orighist_ylabel
    hist_xscale = None
    hist_yscale = hist_valscale
    hist_xlimits = hist_val_limits
    hist_ylimits = hist_freq_limits
    if (is_horiz):
        hist_orient = 'horizontal'
        hist_xlabel = orighist_ylabel
        hist_ylabel = orighist_xlabel
        hist_xscale = hist_valscale
        hist_yscale = None
        hist_xlimits = hist_freq_limits
        hist_ylimits = hist_val_limits

    n, bins, patches = hist_axes.hist(signal, edgecolor=hist_edgecolor, bins=bins_set, density=density_set, linewidth=hist_lwidth, orientation=hist_orient)

    for patch in patches:
        random_color = random.choice(rainbow_colors)
        patch.set_facecolor(random_color)
        patch.set_edgecolor(random_color)
    common_axes_personalization_raw(hist_axes, hist_title, hist_xlabel, hist_ylabel, hist_grid_reqd, hist_xscale, hist_yscale, hist_xlimits, hist_ylimits, hist_bgcolor)

    logger.debug('Subplot created (' + opdesc + ')')
