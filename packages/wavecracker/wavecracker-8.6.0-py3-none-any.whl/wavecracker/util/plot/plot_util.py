# v. 8.5.0 231123

import os
from collections.abc import Iterable
import logging
from config_util import get_plotfiles_params, get_plots_tooltip_params, get_badplot_params
import matplotlib.pyplot as plt
from common_util import wrap_string

def add_plot_tooltip(config, ax, tt_params):
    #lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = get_origplot_tooltip_params(config)
    #lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = True, 8, 'round', 'top', 'yellow', 0.3, 0, 1
    lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = get_plots_tooltip_params(config)

    if (lg_enabled):
        textstr = ''
        notes_count = 0
        for tt_param in tt_params:
            if (tt_param[0]):
                if (notes_count > 0):
                    textstr = textstr + '\n'
                textstr = textstr + tt_param[1]
                notes_count = notes_count + 1
        if (notes_count > 0):
            leg_props = dict(boxstyle=lg_boxstyle, facecolor=lg_bgcolor, alpha=float(lg_transp))
            ax.text(float(lg_xpos), float(lg_ypos), textstr, transform=ax.transAxes, fontsize=int(lg_fontsz), verticalalignment=lg_vertalign, bbox=leg_props)

#def add_freqplots_tooltip(config, ax, dc_offset_suppr):
#    logger = logging.getLogger(__name__)
#    lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos = get_plots_tooltip_params(config)
#    if (lg_enabled):
#        logger.debug('Adding frequency tooltip for subplot at ax: ' + get_ax_asstring(ax))
#        #textstr = ''
#        #notes_count = 0
#        if (dc_offset_suppr):
#            textstr = '-DC offset'
#            #notes_count = notes_count + 1
#            leg_props = dict(boxstyle=lg_boxstyle, facecolor=lg_bgcolor, alpha=float(lg_transp))
#            ax.text(float(lg_xpos), float(lg_ypos), textstr, transform=ax.transAxes, fontsize=int(lg_fontsz), verticalalignment=lg_vertalign, bbox=leg_props)
#            #leg_props = dict(boxstyle='round', facecolor='yellow', alpha=0.3)
#            #ax.text(0, 1, textstr, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=leg_props)

#def eval_subplot_title(channelset_name, channel_xfield, channel_yfield, channel_name, subplot_shortdesc):
#    c_part = 'Plot' if (channel_name is None) else channel_name
#    xfld_part = '' if ((channel_xfield is None) or (len(channel_xfield) < 1)) else '[x: ' + channel_xfield + ']'
#    yfld_part = '' if ((channel_yfield is None) or (len(channel_yfield) < 1)) else '[y: ' + channel_yfield + ']'
#    cs_part = '' if ((channelset_name is None) or (len(channelset_name) < 1)) else '[set: ' + channelset_name + ']'
#    shdesc_part = '' if ((subplot_shortdesc is None) or (len(subplot_shortdesc) < 1)) else ' (' + subplot_shortdesc + ')'
#    print ('\n\n ' + c_part + shdesc_part + ' \n\n')
#    return cs_part + xfld_part + yfld_part + ' ' + c_part + shdesc_part

def hide_empty_subplot(generic_axes):
    logger = logging.getLogger(__name__)
    if not generic_axes.lines:
        if not generic_axes.has_data():
            logger.debug('Found unused subplot: ' + get_ax_asstring(generic_axes) + ', emptying')
            #generic_axes.set_visible(False)
            #generic_axes.set_facecolor('lightgray')
            generic_axes.clear()
            generic_axes.set_axis_off() #generic_axes.axis('off')

#needed, or axes and ticks would be visible - bugged, works fine only when called against individual subplot
def hide_empty_subplots(plt, axes, empty_wspace, empty_hspace):
    logger = logging.getLogger(__name__)
    logger.debug('Emptying unused subplots (wspace=' + str(empty_wspace) + ', hspace=' + str(empty_hspace) + ')')
    try:
        plt.subplots_adjust(wspace=empty_wspace, hspace=empty_hspace)
        if hasattr(axes, 'flat') and isinstance(axes.flat, Iterable):
            for ax in axes.flat:
                hide_empty_subplot(ax)
        else: # when grid is 1x1 it goes here
            #logger.info('placeholder xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            hide_empty_subplot(axes)
    except Exception as e:
        errmsg = str(e)
        #logger.exception('Minor error when emptying an unused subplot: ' + errmsg)
        logger.warn('Minor error when emptying an unused subplot: ' + errmsg)


def get_ax_asstring(ax):
    bbox = ax.get_position()
    # Extract x and y coordinates
    x_pos = bbox.x0
    y_pos = bbox.y0
    #x_pos, y_pos = ax.get_subplotspec().get_topmost_subplotspec().get_gridspec().get_subplot_params().get_position()
    return  '{id: '+ str(id(ax)) + ', x: ' + str(x_pos) + ', y: ' + str(y_pos) + '}' if (not (ax is None)) else '{n.a.}'

def handle_subplot_err(config, target_ax, plot_desc, err_msg):
    logger = logging.getLogger(__name__)
    try:
        base_msg, with_err_msg, max_cols, max_len, x_pos, y_pos, x_text, y_text, fcolor, fshrink, mut_scale  = get_badplot_params(config)
        annot_msg = wrap_string(base_msg + (': ' + err_msg if with_err_msg else ''), max_cols, max_len)
        logger.debug('Annotating problematic subplot at ax: ' + get_ax_asstring(target_ax))
        target_ax.annotate(annot_msg, xy=(x_pos, y_pos), xytext=(x_text, y_text),
                   arrowprops=dict(facecolor=fcolor, shrink=fshrink, mutation_scale=mut_scale))
                   #arrowprops=dict(facecolor='red', shrink=0.05, mutation_scale=20), fontsize=16)
        logger.error('Rendering error (' + plot_desc + '): ' + err_msg)
    except Exception as ehe:
        err_msg_nested = str(ehe)
        logger.exception('Badplot symbol rendering error occurred, during another error: ' + err_msg_nested + ' (root error was: ' + err_msg + ')')

def common_axes_personalization(target_axes, title, xlabel, ylabel, grid_required, yscale, x_boundaries, y_boundaries, bgcolor):
    common_axes_personalization_raw(target_axes, title, xlabel, ylabel, grid_required, None, yscale, x_boundaries, y_boundaries, bgcolor)

def common_axes_personalization_raw(target_axes, title, xlabel, ylabel, grid_required, xscale, yscale, x_boundaries, y_boundaries, bgcolor):
    logger = logging.getLogger(__name__)
    logger.debug('Personalizing subplot at ax: ' + get_ax_asstring(target_axes))
    target_axes.set_title(title)
    target_axes.set_xlabel(xlabel)
    target_axes.set_ylabel(ylabel)
    if (not (xscale is None)):
        target_axes.set_xscale(xscale)
    if (not (yscale is None)):
        target_axes.set_yscale(yscale)
    if (grid_required):
        target_axes.grid(True)
    if (not (bgcolor is None)):
        target_axes.set_facecolor(bgcolor)
    override_axis_boundaries(target_axes, 'x', x_boundaries)
    override_axis_boundaries(target_axes, 'y', y_boundaries)

def override_axis_boundaries(target_axes, axis_type, new_boundaries):
    logger = logging.getLogger(__name__)
    if (not (new_boundaries is None)) and (len(new_boundaries) == 2):
        logger.debug('Overriding axes boundaries for subplot at ax: ' + get_ax_asstring(target_axes))
        val_min = new_boundaries[0]
        val_max = new_boundaries[1]
        if (axis_type == 'x'):
            target_axes.set_xlim(float(val_min), float(val_max))
        if (axis_type == 'y'):
            target_axes.set_ylim(float(val_min), float(val_max))
