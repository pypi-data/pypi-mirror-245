# v. 8.2.0 231121

import os
import matplotlib.pyplot as plt

from config_util import get_plotfiles_params, get_subplotfiles_params
from common_util import get_formatted_tstamp
#from file_util import get_file_basename

import logging

def save_plots(datafile_name, iter_token, config_hnd, out_directory, out_overwrite, subpl_diction, ui_is_multitab, plot_out_mode):
    logger = logging.getLogger(__name__)
    p_out_mode = plot_out_mode
    if (ui_is_multitab):
        p_out_mode = plot_out_mode if (plot_out_mode and (plot_out_mode == 'none')) else 'multi'
        logger.debug('plot-out mode re-assessed to: ' + p_out_mode)
    save_plots_impl(datafile_name, iter_token, config_hnd, out_directory, out_overwrite, subpl_diction, p_out_mode)

def save_plots_impl(datafile_name, iter_token, config_hnd, out_directory, out_overwrite, subpl_diction, plot_out_mode):
    all_option = 'all'
    all_in_one = (plot_out_mode in ['single', all_option])   #'none', 'single', 'multi', 'all'
    split_plots = (plot_out_mode in ['multi', all_option])
    logger = logging.getLogger(__name__)
    datafile_name_wo_ext = os.path.splitext(os.path.basename(datafile_name))[0] + (iter_token if iter_token else '')

    f_ext, fname_suffix, tstamp_suff_fmt = get_plotfiles_params(config_hnd)
    x_splot_exp, y_splot_exp = get_subplotfiles_params(config_hnd)
    tstamp_token = '' if (tstamp_suff_fmt is None) else ('-' + get_formatted_tstamp(tstamp_suff_fmt))
    common_target_fname_start = out_directory + '/' + datafile_name_wo_ext + '-' + fname_suffix + tstamp_token
    common_target_fname_end = '.' + f_ext
    num_s_plots = len(subpl_diction)
    any_img_2_save = (all_in_one or split_plots) and (num_s_plots > 0)
    if (any_img_2_save):
        if (os.path.exists(out_directory)):
            if (all_in_one): # one image per all subplots
                out_plots_file = common_target_fname_start + common_target_fname_end
                plot_2_be_written = (out_overwrite or (not os.path.exists(out_plots_file)))
                if (plot_2_be_written):
                    try:
                        # Save the entire figure
                        plt.savefig(out_plots_file)
                        logger.info('Plots saved (all in: ' + out_plots_file + ')')
                    except Exception as ea:
                        errmsga = str(ea)
                        logger.error('Error while saving plot (' + out_plots_file + '): ' + errmsga)
                else:
                    logger.info('Plots not saved (cannot overwrite ' + out_plots_file + ')')

            if (split_plots): # one image per each subplot
                for curr_key in subpl_diction.keys():
                    out_subplot_file = common_target_fname_start + '-' + curr_key + common_target_fname_end
                    subplot_2_be_written = (out_overwrite or (not os.path.exists(out_subplot_file)))
                    if (subplot_2_be_written):
                        try:
                            curr_ax = subpl_diction[curr_key]
                            parent_fig = curr_ax.figure
                            # Save just the portion _inside_ the second axis's boundaries
                            extent = curr_ax.get_window_extent().transformed(parent_fig.dpi_scale_trans.inverted())
                            #curr_ax.figure.savefig(out_subplot_file, bbox_inches=extent)
                            curr_ax.figure.savefig(out_subplot_file, bbox_inches=extent.expanded(x_splot_exp, y_splot_exp))
                            # Pad the saved area by 10% in the x-direction and 20% in the y-direction
                            #parent_fig.savefig(out_subplot_file, bbox_inches=extent.expanded(1.1, 1.2))
                            #subpl_diction[curr_key].savefig(out_subplot_file)
                            logger.info('Plot saved (' + curr_key + ': ' + out_subplot_file + ')')
                        except Exception as e:
                            errmsg = str(e)
                            logger.error('Error while saving subplot (' + curr_key + ', ' + out_subplot_file + '): ' + errmsg)
                    else:
                        logger.info('Plot not saved (cannot overwrite ' + out_plots_file + ')')
        else:
            logger.error('Plots cannot be saved, output directory (' + out_directory + ') does not exist')
    else:
        if (num_s_plots > 0):
            logger.info('No plots saved (per user request)')
