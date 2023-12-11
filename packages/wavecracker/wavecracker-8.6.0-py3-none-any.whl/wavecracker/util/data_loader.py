# v. 7.1.0 231116

import numpy as np
import sys
#import re

from config_util import load_profiles_rcompact, get_loading_config, get_timeslice_info_format, get_timewindow_info_format, get_signal_info_format

#from common_util import remove_non_printable
from multichannel_util import set_numsamples_predownsampling, derive_channelset_info, debug_channelsets, get_cs_aggregates, get_channelset_signals, get_signal_xy_data, set_signal_xy_data, set_x_axis_calc_attributes, set_signal_calc_attributes

from data_loader_resolution import resolve_loader_func

import logging

def downsample_dataset(attempt_idx, downsampl_pct, channelsets):
    logger = logging.getLogger(__name__)
    size_reduced = False
    num_reduced = 0
    chcount = 0
    for channelset in channelsets:
        num_samples_pre = derive_channelset_info(channelset)
        scount = 0
        for signal in get_channelset_signals(channelset):
            time_vals_pre, sig_vals_pre = get_signal_xy_data(signal)
            chcount = chcount + 1
            scount = scount + 1
            size_reduced_tmp, num_samples_tmp, time_values, signal_values = downsample_dataset_signal(attempt_idx, downsampl_pct, num_samples_pre, time_vals_pre, sig_vals_pre)
            if (scount == 1):
                size_reduced, num_samples = size_reduced_tmp, num_samples_tmp
                num_reduced = num_reduced + (1 if size_reduced else 0)
                logger.debug('>>>>>>>>>>>>>>> Signal #' + str(chcount) + ' - assigning size_reduced and num_samples: ' + str(size_reduced) + ', ' + str(num_samples))
            set_signal_xy_data(signal, time_values, signal_values)
            logger.debug('>>>>>>>>>>>>>>> Signal #' + str(chcount) + ' re-assigning x values and y values')
        set_numsamples_predownsampling(channelset, num_samples_pre)
    debug_channelsets(attempt_idx, channelsets, 'after downsampling')
    return num_reduced, channelsets

def downsample_dataset_signal(attempt_idx, downsampl_pct, num_sampl_pre, time_vals_pre, sig_vals_pre):
    logger = logging.getLogger(__name__)
    size_reduced, num_samples, time_values, signal_values = False, num_sampl_pre, time_vals_pre, sig_vals_pre
    # Specify the downsampling factor (e.g., 2 for 50% samples, 10 for 10% samples)
    #downsampling factor = 100 / (% campioni da tenere)
    #If you want to keep 50% of the samples, the downsampling factor would be 100/50 = 2
    #If you want to keep 10% of the samples, the downsampling factor would be 100/10 = 10
    #If you want to keep 25% of the samples, the downsampling factor would be 100/25 = 4

    # TBD: to resolve with more than 50!

    downsampling_factor_float = 100 / downsampl_pct
    downsampling_factor = int (downsampling_factor_float)
    #logger.info('[' + str(attempt_idx) + '] Downsampling factor rounding: ' + str(downsampling_factor_float) + ' -> ' + str(downsampling_factor))
    # Calculate the indices to preserve
    logger.info('[' + str(attempt_idx) + '] Downsampling attempt ongoing (pct: ' + str(downsampl_pct) + ', factor: ' + str(downsampling_factor_float) + ' -> ' + str(downsampling_factor) + ') ...')

    preserved_indices = np.arange(0, num_sampl_pre, downsampling_factor)
    num_samples_new = len(preserved_indices)
    size_reduced = (num_samples_new > 1) and (num_samples_new < num_sampl_pre)
    if (size_reduced):
        num_samples = num_samples_new
        # Downsample the signal
        time_values = time_vals_pre[preserved_indices]
        signal_values = sig_vals_pre[preserved_indices]

    return size_reduced, num_samples, time_values, signal_values

def post_load_calc(is_after_downsampling, attempt_idx, config, channelsets):
    dataload_ok = 0
    chcount = 0
    for channelset in channelsets:
        #print(' 1------------  DATALOADER.POSTLOAD.129   ' + str(len(channelsets)))
        #x_axis = channelset['x_axis']
        num_samples = derive_channelset_info(channelset)
        scount = 0
        for signal in get_channelset_signals(channelset):
            time_vals, signal_vals = get_signal_xy_data(signal)
            #print ('-------------- array typeZ: ' + str(type(time_vals[0])))
            scount = scount + 1
            chcount = chcount + 1
            data_loaded_signal, sign_avg, average_time_difference = post_load_calc_signal(is_after_downsampling, attempt_idx, config, num_samples, time_vals, signal_vals)
            if (scount == 1):
                #print('xxxxxxxxxxxxxxxxxxxxxxxxxx DEV data_loader.138 before set_x_axis_calc_attributes: ' + str(average_time_difference))
                set_x_axis_calc_attributes(channelset, average_time_difference)
                #print(' 2----------------   ' + str(len(channelsets)))
            #print(' 3----------------   ' + str(len(channelsets)))
            #add sign_avg, average_time_difference to channelsset
            set_signal_calc_attributes(signal, sign_avg)
            dataload_ok = dataload_ok + (1 if (data_loaded_signal) else 0)
    dl_ok = ((dataload_ok == chcount) and (chcount > 0) and (num_samples > 0))
    debug_channelsets(attempt_idx, channelsets, 'after post_load_calc (dataload ok: ' + str(dl_ok) +')')
    return dl_ok, channelsets


def post_load_calc_signal(is_after_downsampling, attempt_idx, config, num_samples, time_vals, signal_vals):
    logger = logging.getLogger(__name__)
    is_time_val_ok = not ((time_vals is None) or (0 == len(time_vals)))
    is_sig_val_ok = not ((signal_vals is None) or (0 == len(signal_vals)))
    data_loaded, sig_avg, average_time_difference = False, None, None

    data_loaded = (num_samples > 0) and (is_time_val_ok)
    if ((not is_time_val_ok) and (num_samples > 0)):
        logger.error('Despite samples were found, x-axis array is EMPTY (this can happen in a multi-channel scenario. Check your data, or contact development)')

    if (is_after_downsampling):
        logger.info('[' + str(attempt_idx) + '] Re-assessing input data summary after downsampling')
    common_nsam_prefix = '[' + str(attempt_idx) + '] Num. of samples'
    common_nsam_info = ': ' + str(num_samples)
    if (is_after_downsampling):
        logger.info(common_nsam_prefix + ' after downsampling' + common_nsam_info)
    else:
        logger.info(common_nsam_prefix + common_nsam_info)

    # Calculate the average time difference between consecutive samples

    average_time_difference = None if ((time_vals is None) or (len(time_vals) < 2)) else np.mean(np.diff(time_vals))
    closure_msg_prefix = '[' + str(attempt_idx) + '] Dataset ingestion attempt completed'
    if (num_samples > 0):
        common_nsample_info = ': ' + str(num_samples) + ')'
        if (is_after_downsampling):
            logger.info(closure_msg_prefix + ' successfully (data points after downsampling' + common_nsample_info)
        else:
            logger.info(closure_msg_prefix + ' successfully (data points' + common_nsample_info)
    else:
        logger.warn(closure_msg_prefix + ', NO DATA FOUND')

    if (data_loaded):
        if (not is_after_downsampling):
            logger.info('[' + str(attempt_idx) + '] Data were loaded successfully (loading attempts performed: ' + str(attempt_idx) + ')')

        #if (is_time_val_ok):
        fmt_time_wnd = get_timewindow_info_format(config) #'.20E'
        common_time_wnd_prefix = '[' + str(attempt_idx) + '] Signal sample time window'
        #if ((time_vals is None) or (0 == len(time_vals))):
        #    common_time_wnd_str = ': [min(x axis): n.a., max(x axis): n.a.]'
        #else:
        common_time_wnd_str = ': [' + format(np.min(time_vals), fmt_time_wnd) + ', ' + format(np.max(time_vals), fmt_time_wnd) + ']'

        if (is_after_downsampling):
            logger.info(common_time_wnd_prefix + ' after downsampling' + common_time_wnd_str)
        else:
            logger.info(common_time_wnd_prefix + common_time_wnd_str)

        if (num_samples > 1):
            min_time_difference = np.min(np.diff(time_vals))
            max_time_difference = np.max(np.diff(time_vals))
            fmt_timesl = get_timeslice_info_format(config) #'.20E'
            common_tsl_info_prefix = '[' + str(attempt_idx) + '] Signal sample time slices AVG (MIN/MAX)'
            common_tsl_info = ': ' + format(average_time_difference, fmt_timesl) + ' (' + format(min_time_difference, fmt_timesl) + '/' + format(max_time_difference, fmt_timesl) + ')'
            if (is_after_downsampling):
                logger.info(common_tsl_info_prefix + ' after downsampling' + common_tsl_info)
            else:
                logger.info(common_tsl_info_prefix + common_tsl_info)

        #common_sv_info_prefix = '[' + str(attempt_idx) + '] Signal sample values AVG (MIN/MAX)'
        common_sv_info_prefix = '[' + str(attempt_idx) + '] Signal sample values AVG/MIN/MAX (S)'
        if (not is_sig_val_ok):
            logger.error(common_sv_info_prefix + ': cannot be calculated! (signal values MISSING)')
        else:
            fmt_sigval = get_signal_info_format(config) #'.20E'
            sig_avg = np.mean(signal_vals)
            sig_min = np.min(signal_vals)
            sig_max = np.max(signal_vals)
            sig_std_dev = np.std(signal_vals)
            #common_sv_info = ': ' + format(sig_avg, fmt_sigval) + ' (' + format(sig_min, fmt_sigval) + '/' + format(sig_max, fmt_sigval) + ')'
            common_sv_info = ': ' + format(sig_avg, fmt_sigval) + '/' + format(sig_min, fmt_sigval) + '/' + format(sig_max, fmt_sigval) + ' (' + str(sig_std_dev) + ')'
            if (is_after_downsampling):
                logger.info(common_sv_info_prefix + ' after downsampling' + common_sv_info)
            else:
                logger.info(common_sv_info_prefix + common_sv_info)

    return data_loaded, sig_avg, average_time_difference

class DataLoader:
    def __init__(self, config_hnd, datafile_name, downsampl, loader_opts):
    #def __init__(self, config_hnd, datafile_name, sorting_choice, audio_channel_arr, on_bad_linec, on_nanc, downsampl):
        self.cfg_hnd = config_hnd
        self.datafile_fpath = datafile_name
        self.loader_options = loader_opts
        #self.sort_choice = sorting_choice
        #self.audio_channels = audio_channel_arr
        #self.on_bad_line = on_bad_linec
        #self.on_nan = on_nanc
        self.downsampling_pct = downsampl

    def load(self):
        logger = logging.getLogger(__name__)
        num_reduced = 0
        num_channels_ret = 0
        samples_count_ok = True
        channelsets = []
        logger.debug('Load begin. Dataset: ' + self.datafile_fpath)

        attempts_done = 0
        data_loaded = False
        num_loading_profiles, ld_profiles_are_compact = load_profiles_rcompact(self.cfg_hnd)
        if (num_loading_profiles < 1):
            raise Exception('MISSING LOADING PROFILES. At least one needs to be configured. Check configuration')
        logger.info('Loading profiles found: ' + str(num_loading_profiles))
        if (not ld_profiles_are_compact):
            logger.warning('Loading profiles sequence has GAPS: loading profiles should be starting by 1, and all consecutive')

        attemptLoadingCfgFound, loading_config = get_loading_config(self.cfg_hnd, attempts_done + 1)
        logger.debug('data_loader.load P1 IS PRESENT: ' + str(attemptLoadingCfgFound))
        load_last_err = None
        while (attemptLoadingCfgFound and (not data_loaded)):
            try:
                attempts_done = attempts_done + 1
                loader_function, loader_function_name, is_overridden, resolut_failure = resolve_loader_func(self.cfg_hnd, loading_config, self.datafile_fpath)
                logger.info('Loader function resolved: ' + loader_function_name + ' (was overridden: ' + str(is_overridden) + ', initial resolution error: ' + str(resolut_failure) + ')')

                loader_params = {'root_cfg': self.cfg_hnd,
                                 'loading_cfg': loading_config,
                                 'attempt_idx': attempts_done,
                                 'options_dictionary': self.loader_options,
                                 'dfile_path': self.datafile_fpath}
                logger.debug('Calling loader function (' + loader_function_name + '), loader options are: ' + str(self.loader_options))
                load_fun_out = loader_function(**loader_params)
                logger.debug(' \n\n\n loader output (' + str(len(load_fun_out)) + '): ' + str(load_fun_out) + '  \n\n\n ')
                samples_count_ok, channelsets = load_fun_out[0], load_fun_out[1]
                num_channels_ret, min_samples, max_samples = get_cs_aggregates(channelsets)
                logger.info('Signals retrieved: ' + str(num_channels_ret) + ', samples (min/max): ' + str(min_samples) + '/' + str(max_samples))

                if ((num_channels_ret > 0) and (not samples_count_ok)):
                    logger.warn('[' + str(attempts_done) + '] *** Num. of samples COULD be inaccurate across different columns. Check input data ***')
                    logger.warn('[' + str(attempts_done) + '] *** NOTE: this could be normal in case of multimedia files from which you are extracting interleaved signals ***')

                #channelsets deve essere popolato con sigX_avg, average_ztime_difference a livello di asse
                data_loaded, channelsets = post_load_calc(False, attempts_done, self.cfg_hnd, channelsets)
            except Exception as e:
                data_loaded = False
                load_last_err = str(e)
                logger.exception('[' + str(attempts_done) + '] Data loader error: ' + load_last_err)
            if (not data_loaded):
                attemptLoadingCfgFound, loading_config = get_loading_config(self.cfg_hnd, attempts_done + 1)

        ############################# fine loop di caricamento - gli N tentativi insomma
        #print ('CHANNELS SETS AFTER LOOP' + channelsets_as_string(channelsets))
        if (data_loaded):
            logger.info('Data were loaded successfully (loading attempts performed: ' + str(attempts_done) + ')')

            # Downsampling
            if (self.downsampling_pct > 0):
                #downsample ora deve popolare campi aggiuntivi di tutti i segnali con tempi e valori "downsamplati"
                num_reduced, channelsets = downsample_dataset(attempts_done, self.downsampling_pct, channelsets)
                if (num_reduced > 0):
                    logger.info('[' + str(attempts_done) + '] Downsampling performed (channel sets reduced: ' + str(num_reduced) + ')')
                    data_loaded, channelsets = post_load_calc(True, attempts_done, self.cfg_hnd, channelsets)
                else:
                    logger.warn('[' + str(attempts_done) + '] Downsampling did not take place (maybe no reduction took place, or remaining samples would not be enough - check data)')

        debug_channelsets(attempts_done, channelsets, 'right before the LOAD.return [' + str((data_loaded, load_last_err, attempts_done)) + ']')
        #return data_loaded, channelsets, load_last_err, attempts_done, num_samples_cpre, num_csamples
        return data_loaded, channelsets, load_last_err, attempts_done, None, None
