# v. 8.6.0 231211

import os
import sys
import argparse
import logging
from datetime import datetime

SAROOT = os.path.dirname(os.path.abspath(__file__))
sa_scripts_util=SAROOT + '/util'
sys.path.append(sa_scripts_util)
sys.path.append(sa_scripts_util + '/dataloaders')
sys.path.append(sa_scripts_util + '/plot')

diagnost_on = False
try:
    from boot_helper import boot_checks
    diagnost_on = boot_checks()
except Exception as e:
    print('[BOOT][WARN] Boot checks could not be performed [error: ' + str(e) + ']')

from common_util import log_app_banner, print_diagnostics, register_os_sig_handlers
from config_util import get_config_hnd, get_origsignalplot_title #get_tables_conf_hnd, 
from logging_util import init_logging
from data_loader import DataLoader
from data_preproc import DataPreprocessor
from ft_calculator import SignalTransformer
from plot_manager import PlotsBuilder
from plot_save import save_plots
from file_util import save_ft_data, create_files_list, check_critical_files
from multichannel_util import derive_channelset_info, get_channelset_signals, get_channelset_attributes, get_signal_attributes, get_signal_data, debug_channelsets
from polynt_calc import eval_polynt_data

def process_datasets(
        input_path,
        qplot,
        table_def,
        input_datafile_extensions,
        #sort,
        on_bad_line,
        on_nan,
        remove_dc_offset,
        downsampling,
        frequency_filter,
        #decimal_sep,
        #alt_decimal_sep,
        out_directory,
        out_overwrite,
        plot_out,
        data_out,
        data_out_merged,
        plot_signal_time_window,
        plot_signal_ampl_window,
        plot_ft_freq_window,
        plot_ft_magn_window,
        plot_psd_freq_window,
        plot_psd_pow_window,
        plot_hist_val_window,
        plot_hist_freq_window,
        plot_ftphase_freq_window,
        plot_ftphase_val_window,
        exclude_orig,
        exclude_ft,
        include_phase,
        include_spectrogram,
        include_3d_spectrogram,
        include_envelope,
        include_psd,
        include_histogram,
        include_wl_transform,
        include_qq,
        include_inst_freq,
        dedicated_tab,
        plot_noshow,
        audio_channels,
        simple_ui,
        poly_int,
        conf,
        tables_conf,
        log_conf,
        diagnostics_on
    ):
    #init_logging(log_conf, ['PIL', 'h5py._conv'])
    init_logging(log_conf, [])
    logger = logging.getLogger(__name__)

    multitab_ui = not simple_ui
    #cc_result, missf = check_critical_files([conf, tables_conf])
    cc_result, missf = check_critical_files([conf])
    if (not cc_result):
        logger.critical('Critical files missing: ' + str(missf))
        logger.critical('Check configuration, and try again')
        sys.exit(1)

    config_hnd =      get_config_hnd(True,      'main',   conf)
    tables_conf_hnd = get_config_hnd(False, 'tables', tables_conf) #get_tables_conf_hnd(config_hnd, tables_conf)
    if (not tables_conf_hnd):
        logger.warning('This may be relevant only when using CSV (and not all the times). Check configuration ONLY if warning about issues in defining the table show up later in the log')

    # misc init activities
    log_app_banner()
    print_diagnostics(diagnostics_on)
    register_os_sig_handlers()
    #file_extensions_str = 'txt,csv'
    datasets, num_items = create_files_list(input_path, input_datafile_extensions)

    num_loaded, num_processed, num_errors = 0, 0, 0

    out_direct = out_directory
    if (num_items > 0):
        logger.info('Processing loop over datasets: begin')
        if (not out_direct):
            out_direct = datetime.now().strftime('./out_%Y%m%d%H%M%S')
            os.makedirs(out_direct)
            logger.info('Output directory created: ' + out_direct)

    items_count = 0
    for dataset in datasets:
        dataset_filename = str(dataset)
        items_count = items_count + 1
        logger.info('Dataset[' + str(items_count) + '/' + str(num_items) + ']: ' + dataset_filename)
        try:
            plot_out_main = True # per salvare la jpeg con tutti i grafici
            load_ok, process_ok = process_dataset(dataset_filename,
                qplot,
                table_def,
                #sort,
                on_bad_line,
                on_nan,
                remove_dc_offset,
                downsampling,
                frequency_filter,
                out_direct,
                out_overwrite,
                plot_out,
                data_out,
                data_out_merged,
                plot_signal_time_window,
                plot_signal_ampl_window,
                plot_ft_freq_window,
                plot_ft_magn_window,
                plot_psd_freq_window,
                plot_psd_pow_window,
                plot_hist_val_window,
                plot_hist_freq_window,
                plot_ftphase_freq_window,
                plot_ftphase_val_window,
                not exclude_orig,
                not exclude_ft,
                include_phase,
                include_spectrogram,
                include_3d_spectrogram,
                include_envelope,
                include_psd,
                include_histogram,
                include_wl_transform,
                include_qq,
                include_inst_freq,
                dedicated_tab,
                plot_noshow or (num_items > 1),
                audio_channels,
                multitab_ui,
                poly_int,
                config_hnd,
                tables_conf_hnd)
            num_loaded = num_loaded + 1 if load_ok else num_loaded
            num_processed = num_processed + 1 if process_ok else num_processed
        except Exception as e:
            num_errors = num_errors + 1
            errmsg = str(e)
            logger.exception('Error: ' + errmsg)

    if (num_items > 1):
        logger.info('Processing loop over datasets complete. Summary:')
        logger.info('    Items:  ' + str(num_items))
        logger.info('    Loaded: ' + str(num_loaded))
        logger.info('    Ok:     ' + str(num_processed))
        logger.info('    Fails:  ' + str(num_errors))
    logger.info('Program terminated')

def process_dataset(
        datafile_name,
        qplot,
        table_def,
        #sort_choice,
        on_bad_line,
        on_nan,
        remove_dc_offset,
        downsampling,
        frequency_filter,
        out_directory,
        out_overwrite,
        plot_out_mode,
        data_out_mode,
        data_out_merged_mode,
        plot_signal_time_window,
        plot_signal_ampl_window,
        plot_ft_freq_window,
        plot_ft_magn_window,
        plot_psd_freq_window,
        plot_psd_pow_window,
        plot_hist_val_window,
        plot_hist_freq_window,
        plot_ftphase_freq_window,
        plot_ftphase_val_window,
        include_original,
        include_ftransf,
        include_phase,
        include_spectrogram,
        include_3d_spectrogram,
        include_envelope,
        include_psd,
        include_histogram,
        include_wl_transform,
        include_qq,
        include_inst_freq,
        dedicated_tabs,
        plot_noshow,
        audio_channel_arr,
        multitab_ui,
        poly_int,
        config_hnd,
        tables_conf_hnd
    ):
    logger = logging.getLogger(__name__)
    data_loaded, data_processed = False, False
    # Load Data
    #print ('qplot: ['Time(s)', 'Channel1']
    loader_options = {
       'audio': {
           'channels': audio_channel_arr
       },
       'csv': {
           'on_bad_lines': on_bad_line,
           'on_nans': on_nan,
           'cmdline_tabledef_params': qplot,
           'table_def_override': table_def,
           'table_conf': tables_conf_hnd
       }
    }
    sigdataloader = DataLoader(config_hnd, datafile_name, downsampling, loader_options)
    data_loaded, channelsets, load_last_err, attempts, _, _ = sigdataloader.load()

    #debug_channelsets(None, channelsets, 'out of load')
    channel_count = 0
    plot_save_op_count = 0
    data_save_op_count = 0
    #ui_is_multitab = multitab_ui
    if (not data_loaded):
        logger.info('No processing took place (no data; loading attempts performed: ' + str(attempts) + ')')
        if (not load_last_err is None):
          logger.info('Last data loading error was: ' + load_last_err)
    else:
        #if (num_samples > 1):
        origsubplot_type_label, origplotname = get_origsignalplot_title(config_hnd)
        cs_index = 0;
        for channelset in channelsets:
            cs_index = cs_index + 1;
            channelset_name = 'cs' + str(cs_index)
            cnum_samples = derive_channelset_info(channelset) #len(get_channelset_signals(channelset)[0]['x_data'])
            #print('********** DEV WARN - [main.281] num_samples_pre to be set into the channelset at load time / all loaders not to return num samples and num_samples_pre,')
            #channelset, x_axis, must expose num samples and maybe even the PRE')
            if (cnum_samples > 1):
                sgn_index = 0;
                channel_xfield, channel_xlabel, average_x_difference, x_filenametoken, cnum_samples_pre = get_channelset_attributes(channelset)
                #channel_xlabel = channel_xfield #############################################
                frequencies_list, fft_magn_list, y_fields_list = [], [], []
                for cur_channel in get_channelset_signals(channelset):
                    channel_count = channel_count + 1
                    sgn_index = sgn_index + 1;
                    channel_yfield, channel_ylabel, y_filenametoken = get_signal_attributes(cur_channel)
                    logger.debug('Processing signal entry [' + str(cs_index) + '][' + str(channel_count) + '] ...')
                    logger.info('SIGNAL PROCESSING - BEGIN (' + channel_xfield + ', ' + channel_yfield + ')')
                    time_vals, signal_vals, signal_avg = get_signal_data(cur_channel)
                    # Preprocess Data
                    preprocessor = DataPreprocessor(signal_vals, signal_avg, remove_dc_offset)
                    signal_vals = preprocessor.preprocess()

                    # Calculate Fourier transform
                    sigtransformer = SignalTransformer(config_hnd, cnum_samples, average_x_difference, signal_vals, include_envelope, include_phase, include_psd, frequency_filter, include_wl_transform, include_inst_freq)
                    num_freq_vals, sampling_freq, frequencies, signal_fft, signal_fft_magnitude, signal_ft_phase, signal_filtered_vals, signal_peaks_vals, psd_x_vals, psd_y_vals, wv_scales, wavelet_transform_data, wavelet_type, instant_freq = sigtransformer.transform()

                    # Calculate interpolations
                    #poly_int = ['5:0.1,0.3', '3:0.6,0.62']
                    polynt_data = eval_polynt_data(cs_index, channel_count, poly_int, time_vals, signal_vals)

                    pbuilder = None
                    subplots_dict = {}
                    #plots_saved = False
                    #dfiles_saved = False
                    x_ftoken = '-' + x_filenametoken
                    iter_ftoken = x_ftoken + '-' + y_filenametoken
                    # if plot_noshow and plot_out_mode no save ...qui sotto non dovrei entrarci
                    try:
                        # Create plots
                        pbuilder = PlotsBuilder(multitab_ui, dedicated_tabs, config_hnd, channelset_name, channel_xfield, channel_yfield, channel_xlabel, channel_ylabel, origplotname, origsubplot_type_label, include_original, include_ftransf, datafile_name, cnum_samples_pre, cnum_samples, num_freq_vals, sampling_freq, remove_dc_offset, time_vals, plot_signal_time_window, signal_vals, signal_peaks_vals, signal_filtered_vals, frequencies, signal_fft_magnitude, plot_ft_magn_window, plot_signal_ampl_window, plot_ft_freq_window, signal_ft_phase, plot_psd_freq_window, plot_psd_pow_window, plot_hist_val_window, plot_hist_freq_window, plot_ftphase_freq_window, plot_ftphase_val_window, include_spectrogram, include_3d_spectrogram, include_histogram, psd_x_vals, psd_y_vals, wv_scales, wavelet_transform_data, wavelet_type, include_qq, polynt_data, instant_freq)
                        subplots_dict = pbuilder.createPlots()
                        try:
                            # Save plots if possible
                            save_plots(datafile_name, iter_ftoken, config_hnd, out_directory, out_overwrite, subplots_dict, multitab_ui, plot_out_mode)
                            plots_saved = True
                            plot_save_op_count = plot_save_op_count + 1
                        except Exception as pp:
                            pp_errmsg = str(pp)
                            logger.exception('Plotting persistence related error: ' + pp_errmsg)
                    except Exception as ierr:
                        i_errmsg = str(ierr)
                        logger.exception('Plotting related error: ' + i_errmsg)

                    try:
                        #data_out_merged_mode
                        #Save frequency and magnitude to a CSV file - I tried to parallelize. Some issue with that. Under analysis
                        if (not data_out_merged_mode):
                            cols_saved = save_ft_data(datafile_name, iter_ftoken, config_hnd, out_directory, out_overwrite, [frequencies], [signal_fft_magnitude], [channel_ylabel], data_out_mode)
                            #print('>>>>>>>>>>>>>>< POST1 ' + str(cols_saved))
                            data_save_op_count = data_save_op_count + cols_saved
                        else:
                            frequencies_list.append(frequencies)
                            fft_magn_list.append(signal_fft_magnitude)
                            y_fields_list.append(channel_ylabel)
                    except Exception as derr:
                        d_errmsg = str(derr)
                        logger.exception('Data persistence related error: ' + d_errmsg)

                    # Display plots if required
                    if (not (pbuilder is None)) and (not plot_noshow):
                        logger.info('Plots are being displayed (source: ' + datafile_name + '). You can close the plots window to terminate the program')
                        try:
                            pbuilder.showPlots()
                        except Exception as perr:
                            p_errmsg = str(perr)
                            logger.exception('UI-related error: ' + p_errmsg)
                if (data_out_merged_mode):
                    cols_saved = save_ft_data(datafile_name, x_ftoken, config_hnd, out_directory, out_overwrite, frequencies_list, fft_magn_list, y_fields_list, data_out_mode)
                    #print('>>>>>>>>>>>>>>< POST2 ' + str(cols_saved))
                    data_save_op_count = data_save_op_count + cols_saved
            else:
                logger.warning('AXIX ' + channel_xfield + ' IS TOO LOW ON SAMPLES (total: ' + str(cnum_samples) + '), not enough for any output to be produced')
            ############### end if cnumsamples > 1


        data_processed = ((plot_save_op_count == channel_count) and (data_save_op_count == channel_count))

    return data_loaded, data_processed

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, default='./data/sample.csv', help='input CSV file (s), you can specify a file or a directory (and in such case, all of its files - NOT recursively - will be processed)')
    #parser.add_argument('--qplot', action='append', nargs='+', type=str, default=None, help='Quick Plot. specify directly column names, the first being X (--qplot time(s) Channel1 Channel2 for example) for quick processing, the first one is assumed to be an x axis, then the Ys come - no need of having a table defined')
    #parser.add_argument('--qplot', type=str, default=None, help='Quick Plot. Specify directly column names, the first being X (--qplot time(s) Channel1 Channel2 for example) for quick processing, the first one is assumed to be an x axis, then the Ys come - no need of having a table defined')
    parser.add_argument('--qplot', nargs='+', type=str, default=None, help='Quick Plot. Specify directly column names, the first being X (--qplot time(s) Channel1 Channel2 for example) for quick processing, the first one is assumed to be an x axis, then the Ys come - no need of having a table defined')
    parser.add_argument('--table-def', type=str, default=None, help='if specified, overrides the default table definition pointer for the CSV file')
    parser.add_argument('--input-datafile-extensions', nargs='+', type=str, default=None, help='applies if the input path is a directory. These are the extensions allowed')
    #parser.add_argument('--sort', type=str, default='byTime', help='if specified, signal data will be preliminarly sorted, possible values are \'byTime\' or \'byIndex\' or \'byValue\'')
    #parser.add_argument('--sort', type=str, choices=['byTime'], default=None, help='if specified, signal data will be preliminarly sorted, possible values are: \'byTime\'')
    parser.add_argument('--on-bad-line', type=str, choices=['error', 'warn', 'skip'], default='warn', help='csv files discard policy for bad lines')
    parser.add_argument('--on-nan', type=str, choices=['error', 'warn', 'skip', 'keep'], default='error', help='csv files discard policy for NaN values')
    parser.add_argument('--remove-dc-offset', action='store_true', default=False, help='if true, the DC offset is removed from the signal in preprocessing phase')
    parser.add_argument('--downsampling', default=0.0, type=float, help='if present, reduces the number of samples by the specified percentage, example: 10.0 would reduce the samples by 10%, so that if the samples are 1000 we then would go down to 900')
    parser.add_argument('--frequency-filter', nargs='+', type=str, help='sequence of bands (specified as low,high, where the absence of either means infinity) in the filtered signal to display along with the original')
    #parser.add_argument('--decimal-sep', type=str, default='.', help='decimal separator')
    #parser.add_argument('--alt-decimal-sep', type=str, default=',', help='alternate decimal separator')
    parser.add_argument('--out-directory', type=str, default=None, help='output target directory')
    parser.add_argument('--out-overwrite', action='store_true', default=False, help='if true, plots are overwritten if found existing')
    #parser.add_argument('--plot-out-main', action='store_true', default=False, help='if true, the single image with all plots is saved')
    #parser.add_argument('--plot-out-multi', action='store_true', default=False, help='if true, subplots are saved individually')
    parser.add_argument('--plot-out', type=str, choices=['none', 'single', 'multi', 'all'], default='single', help='single is the image with all subplots, multi is one image per subplot, all is all of them')
    parser.add_argument('--data-out', type=str, choices=['none', 'ft', 'all'], default='ft', help='ft is fourier transform, all is all of them')
    parser.add_argument('--data-out-merged', action='store_true', default=False, help='if true, the generated csv will be merged (one per every x axis)')
    parser.add_argument('--plot-signal-time-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s plot, in the time interval of interest')
    parser.add_argument('--plot-signal-ampl-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s plot, in the amplitudes\' interval of interest')
    parser.add_argument('--plot-ft-freq-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s FT plot, in the frequency interval of interest')
    parser.add_argument('--plot-ft-magn-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s FT plot, in the magnitude interval of interest')
    parser.add_argument('--plot-psd-freq-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s PSD plot, in the frequency interval of interest')
    parser.add_argument('--plot-psd-pow-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s PSD plot, in the power interval of interest')
    parser.add_argument('--plot-hist-val-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s histogram plot, in the values interval of interest')
    parser.add_argument('--plot-hist-freq-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s histogram plot, in the frequency interval of interest')
    parser.add_argument('--plot-ftphase-freq-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s FT phase plot, in the frequency interval of interest')
    parser.add_argument('--plot-ftphase-val-window', nargs=2, type=float, help='if specified, allows zooming over the signal\'s FT phase plot, in the frequency interval of interest')
    parser.add_argument('--exclude-orig', action='store_true', default=False, help='if true, the plot will not include the original signal')
    parser.add_argument('--exclude-ft', action='store_true', default=False, help='if true, the plot will not include the FT')
    parser.add_argument('--include-phase', action='store_true', default=False, help='if true, the plot will include the phase')
    parser.add_argument('--include-spectrogram', action='store_true', default=False, help='if true, the plot will include the spectrogram')
    parser.add_argument('--include-3d-spectrogram', action='store_true', default=False, help='if true, the plot will include the 3D spectrogram')
    parser.add_argument('--include-envelope', action='store_true', default=False, help='if true, the plot will include the envelope')
    parser.add_argument('--include-psd', action='store_true', default=False, help='if true, the plot will include the power density spectrum')
    parser.add_argument('--include-histogram', action='store_true', default=False, help='if true, the plot will include the values histogram')
    parser.add_argument('--include-wl-transform', action='store_true', default=False, help='if true, the plot will include the wavelet transform')
    parser.add_argument('--include-qq', action='store_true', default=False, help='if true, the plot will include a configurable Q-Q plot')
    parser.add_argument('--include-inst-freq', action='store_true', default=False, help='if true, the plot will include the instantaneous frequency plot')
    parser.add_argument('--dedicated-tab', nargs='+', type=str, choices=['orig' , 'ft' , 'qq' , 'psd' , 'hist' , 'ft-phase' , 'wvlet' , '3dspctg' , 'spctg'], default=[], help='plots you want to put on a dedicated tab regardless of its grid layout')
    parser.add_argument('--audio-channels', nargs='+', type=str, choices=['mono', 'left', 'right', 'stereo', 'interleaved'], default=['mono'], help='audio channels selected')
    parser.add_argument('--plot-noshow', action='store_true', default=False, help='if true, the plot will be NOT shown on the fly')
    #parser.add_argument('--multitab-ui', action='store_true', default=False, help='if true, the new multitab UI is used')
    parser.add_argument('--simple-ui', action='store_true', default=False, help='if true, the old single-tab UI is used')
    parser.add_argument('--poly-int', nargs='+', type=str, default=[], help='collection of degree:interval_low,interval_hi definitions, for polynomial interpolation')
    parser.add_argument('--conf', type=str, default=SAROOT + '/conf/signal_analyzer.yaml', help='main configuration file')
    parser.add_argument('--tables-conf', type=str, default=SAROOT + '/conf/sa_tables.yaml', help='table definitions file')
    parser.add_argument('--log-conf', type=str, default=SAROOT + '/conf/logging.conf', help='logging configuration file')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    params_dict = vars(opt)

    params_dict['diagnostics_on'] = diagnost_on
    process_datasets(**params_dict)
