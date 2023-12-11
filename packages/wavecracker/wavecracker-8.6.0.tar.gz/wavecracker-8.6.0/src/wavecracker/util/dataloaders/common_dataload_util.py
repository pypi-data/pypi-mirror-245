# v. 4.4.0 231110

import logging
from file_util import detect_encoding, platform_encoding
from common_util import beautified_string, is_stdout_debug_on
import numpy as np
from multichannel_util import build_table_def, build_table_def_from_cmd, load_inmemory_table, build_channelsets

from common_util import is_any_A_in_B

def get_optdict_audio_settings(options_dictionary):
    audio_params_key = 'audio'
    return options_dictionary[audio_params_key] if audio_params_key in options_dictionary else None

def get_optdict_audio_setting(options_dictionary, skey):
    audio_settings = get_optdict_audio_settings(options_dictionary)
    val2ret = audio_settings[skey] if ((audio_settings) and (skey in audio_settings)) else None
    return val2ret

def get_optdict_csv_settings(options_dictionary):
    csv_params_key = 'csv'
    return options_dictionary[csv_params_key] if csv_params_key in options_dictionary else None

def get_optdict_csv_setting(options_dictionary, skey):
    csv_settings = get_optdict_csv_settings(options_dictionary)
    val2ret = csv_settings[skey] if ((csv_settings) and (skey in csv_settings)) else None
    return val2ret

def create_table(attempt_idx, root_cfg, loading_cfg, options_dictionary):
    logger = logging.getLogger(__name__)
    table_def = None
    cmdl_tdef_params_key = 'cmdline_tabledef_params'
    #qplot = options_dictionary[cmdl_tdef_params_key] if (cmdl_tdef_params_key in options_dictionary) else None
    qplot = get_optdict_csv_setting(options_dictionary, cmdl_tdef_params_key)

    #print('xxxxx \n\n\n  ' + str(qplot and (len(qplot) > 1)) + '\n\n\n PPPPPPPPPPPPP')
    if (qplot and (len(qplot) > 1)):
        table_def_id, table_def = build_table_def_from_cmd(attempt_idx, qplot)
        logger.info('[' + str(attempt_idx) + '] Table definition id: ' + table_def_id + ' (in memory, from command line)')
    else:
        if (qplot):
            logger.warning('[' + str(attempt_idx) + '] (x, y) information specified in the command line has been DISCARDED (check configuration), standard tables configuration applies')
        table_conf_hnd, table_defin_override = get_table_conf_ref(options_dictionary)
        table_def_id, table_def = build_table_def(attempt_idx, root_cfg, table_conf_hnd, loading_cfg, table_defin_override)
        logger.info('[' + str(attempt_idx) + '] Table definition id: ' + table_def_id)
    return table_def

def get_table_conf_ref(options_dictionary):
    #logger = logging.getLogger(__name__)
    tc_key = 'table_conf'
    table_def_override_key = 'table_def_override'
    table_conf_hnd = get_optdict_csv_setting(options_dictionary, tc_key)
    table_def_over = get_optdict_csv_setting(options_dictionary, table_def_override_key)
    #table_conf_hnd = options_dictionary[tc_key]
    #table_def_over = options_dictionary[table_def_override_key]
    return table_conf_hnd, table_def_over



def display_columns_metadata(attempt_idx, ctype, cols):
    logger = logging.getLogger(__name__)
    if ((not (cols is None)) and (len(cols) > 0)):
        logger.info('[' + str(attempt_idx) + '] ' + ctype + ' fields found (' + str(len(cols)) + '): ' + ', '.join(cols))

def display_headersearch_metadata(attempt_idx, head_cols, x_cols, y_cols):
    #logger = logging.getLogger(__name__)
    display_columns_metadata(attempt_idx, 'Header', head_cols)
    display_columns_metadata(attempt_idx, 'x-axis', x_cols)
    display_columns_metadata(attempt_idx, 'y-axis', y_cols)

def eval_audio_time_vals(attempt_idx, num_samples, frame_rate):
    logger = logging.getLogger(__name__)
    time_values = np.arange(0, num_samples) / frame_rate
    logger.debug('[' + str(attempt_idx) + '] Time instants array evaluated')
    return time_values

def build_audio_channelsets(attempt_idx, chann_dictionaries, x_field, x_filetoken, frame_rate):
    logger = logging.getLogger(__name__)
    time_vals = None
    audio_channelsets = []
    samples_count_ok = True

    is_psortable = False
    logger.debug('[' + str(attempt_idx) + '] panda-sortable (inbuilt due to audio nature): ' + str(is_psortable))

    distinct_numsamples = list(set(len(item['audiodata']) for item in chann_dictionaries))

    #print ('-------------------------> distinct values for num of samples: ' + str(distinct_numsamples))
    chcount = 0
    count_mismatches_count = 0
    for curr_num_signal_samples in distinct_numsamples:
        chcount = chcount + 1
        matching_chdictionaries = [item for item in chann_dictionaries if len(item['audiodata']) == curr_num_signal_samples]
        #print('---------> names for ' + str(curr_num_signal_samples) + ': ' + ', '.join(item['yname'] for item in matching_chdictionaries))
        cur_x_field = x_field + '_' + str(chcount)

        logger.debug('[' + str(attempt_idx) + '][' + str(curr_num_signal_samples) + '] Num. of audio samples: ' + str(curr_num_signal_samples))
        time_vals = eval_audio_time_vals(attempt_idx, curr_num_signal_samples, frame_rate)

        x_columns_found = [cur_x_field]
        y_columns_found = [d['yname'] for d in matching_chdictionaries]
        y_filetokens_found = [(d['filetoken'] if ('filetoken' in d) else 'NA') for d in matching_chdictionaries]
        #logger.warn('\n\n\n\n[' + str(attempt_idx) + '] build_audio_channelsets: file tokens of the audio file: ' + str(y_filetokens_found))
        #GOOD all_columns = y_columns_found + [cur_x_field]
        raw_audiodata = {item['yname']: item['audiodata'] for item in matching_chdictionaries}
        #logger.debug('\n\n\n\n[' + str(attempt_idx) + '] raw_audiodata: ' +str(raw_audiodata)+ ' \n\n')

        audio_sign_conftable = load_inmemory_table(attempt_idx, cur_x_field,  x_filetoken + str(chcount), y_columns_found, y_filetokens_found)
        #GOOD audio_sign_conftable = load_inmemory_table(attempt_idx, all_columns, cur_x_field)

        #audio_sign_conftable = load_inmemory_table(attempt_idx, ['Time', 'L', 'R'], 'Time')
        #summ_log = ' [' + ', '.join([d['yname'] for d in matching_chdictionaries]) + ']'
        #'audiodata'
        logger.debug('\n\n\n\n[' + str(attempt_idx) + '] build_audio_channelsets - TABLE ' + str(audio_sign_conftable))
        
        #_, _, samples_count_ok, _ is not used
        min_num_sampl, max_num_sampl, _, cur_audio_channelsets = build_channelsets(attempt_idx, audio_sign_conftable, x_columns_found, y_columns_found, None, raw_audiodata, is_psortable, time_vals)
        audio_channelsets.append(cur_audio_channelsets[0])

        #il num samples calcolato dal primo segnale e quello dalla build_channelsets dovrebbero sempre coincidere!
        curr_samp_count_ok = (min_num_sampl == max_num_sampl == curr_num_signal_samples)
        if (not curr_samp_count_ok):
            count_mismatches_count = count_mismatches_count + 1
            logger.error('\n\n\n\n[' + str(attempt_idx) + '][samples: ' + str(curr_num_signal_samples) + '][x: ' + cur_x_field + '] CRITICAL - common_dataload_util.build_audio_channelsets: MISMATCH between num_sampl and num_signal_samples (which should ALWAYS match)')

    logger.debug('\n\n\n\n[' + str(attempt_idx) + '] build_audio_channelsets - CHANNEL SETS: ' + str(audio_channelsets))
    samples_count_ok = (count_mismatches_count > 0)
    #return curr_num_signal_samples, samples_count_ok, audio_channelsets
    return samples_count_ok, audio_channelsets



def get_audio_channels(attempt_idx, options_dictionary, signal_sound_arr_L, signal_sound_arr_R, audio_channels_num, left_audio_idx, right_audio_idx):
    logger = logging.getLogger(__name__)
    #opt_dict_audio_channels_key = 'audio_channels'
    #opts_chosen_orig = options_dictionary[opt_dict_audio_channels_key]
    opt_dict_audio_channels_key = 'channels'
    opts_chosen_orig = get_optdict_audio_setting(options_dictionary, opt_dict_audio_channels_key)
    logger = logging.getLogger(__name__)
    channels_dict = []
    sign_is_mono = True
    mono_opt = 'mono'
    left_opt = 'left'
    right_opt = 'right'
    stereo_opt = 'stereo'
    filetoken_interleaved = 'I'
    interleaved_opt = 'interleaved'
    valid_options = [mono_opt, left_opt, right_opt, stereo_opt, interleaved_opt]
    opts_chosen = [mono_opt]
    if (not (opts_chosen_orig is None)) and (len(opts_chosen_orig) > 0):
        opts_chosen = opts_chosen_orig if is_any_A_in_B(opts_chosen_orig, valid_options) else opts_chosen
    is_left_chosen = is_any_A_in_B(opts_chosen, [left_opt])
    is_interl_chosen = is_any_A_in_B(opts_chosen, [interleaved_opt])
    fname_key = 'yname'
    audiodata_key = 'audiodata'
    filetoken_key = 'filetoken'
    logger.debug('Audio channels choosen: ' + str(opts_chosen))
    sign_is_mono = (audio_channels_num < 2)
    is_mono_log_token = 'mono' if sign_is_mono else 'stereo'
    logger.info('[' + str(attempt_idx) + '] Audio channels found: ' + str(audio_channels_num) + ' (' + is_mono_log_token + ')')
    if (not (opts_chosen is None)) and (len(opts_chosen) > 0):
        left_on = sign_is_mono or is_any_A_in_B(opts_chosen,[mono_opt, left_opt, stereo_opt])
        right_on = (not sign_is_mono) and is_any_A_in_B(opts_chosen, [right_opt, stereo_opt])
        interleaved_on = (not sign_is_mono) and is_any_A_in_B(opts_chosen, [interleaved_opt])
        if (left_on):
            audio_ch_idx = left_audio_idx
            audio_ch_label = 'mono' if (sign_is_mono) else 'left'
            logger.debug('[' + str(attempt_idx) + '] Adding audio channel (' + audio_ch_label + ', index: ' + str(audio_ch_idx) + ', )')
            left_channel_dict = {
                fname_key: str(audio_ch_idx) + '/' + str(audio_channels_num) + ' (' + audio_ch_label + ')',
                audiodata_key: signal_sound_arr_L,
                filetoken_key: str(audio_ch_idx)
            }
            channels_dict.append(left_channel_dict)

        if (right_on):
            audio_ch_idx = right_audio_idx
            audio_ch_label = 'right'
            if (signal_sound_arr_R is None):
                logger.warn('[' + str(attempt_idx) + '] Audio channel was expected BUT NOT FOUND (' + audio_ch_label + ', index: ' + str(audio_ch_idx) + ', )')
            else:
                logger.debug('[' + str(attempt_idx) + '] Adding audio channel (' + audio_ch_label + ', index: ' + str(audio_ch_idx) + ', )')
                right_channel_dict = {
                    fname_key: str(audio_ch_idx) + '/' + str(audio_channels_num) + ' (' + audio_ch_label + ')',
                    audiodata_key: signal_sound_arr_R,
                    filetoken_key: str(audio_ch_idx)
                }
                channels_dict.append(right_channel_dict)

        if (interleaved_on):
            audio_ch_idx_desc = str(left_audio_idx) + '+' + str(right_audio_idx)
            audio_ch_label = 'interleaved'
            interleaved_array = np.column_stack((signal_sound_arr_L, signal_sound_arr_R)).flatten()
            logger.debug('[' + str(attempt_idx) + '] left samples:        ' + str(len(signal_sound_arr_L)))
            logger.debug('[' + str(attempt_idx) + '] right samples:       ' + str(len(signal_sound_arr_R)))
            logger.debug('[' + str(attempt_idx) + '] interleaved samples: ' + str(len(interleaved_array)))

            logger.debug('[' + str(attempt_idx) + '] Adding audio channel (' + audio_ch_label + ', indexes: ' + audio_ch_idx_desc + ')')
            right_channel_dict = {
                fname_key: audio_ch_idx_desc + '/' + str(audio_channels_num) + ' (' + audio_ch_label + ')',
                audiodata_key: interleaved_array,
                filetoken_key: filetoken_interleaved
            }
            channels_dict.append(right_channel_dict)

        debug_channels_dict(attempt_idx, channels_dict, sign_is_mono, is_left_chosen, right_on, is_interl_chosen, 'after creation')
    return channels_dict, sign_is_mono, is_left_chosen, is_interl_chosen

def debug_channels_dict(attempt_idx, channels_dict, sign_is_mono, is_left_chosen, right_on, is_interl_chosen, contextstr):
    logger = logging.getLogger(__name__)
    cd_show = is_stdout_debug_on()
    context = '' if (contextstr is None) else ' (' + contextstr + ')'
    mode_info = 'mono: ' + str(sign_is_mono) + '\nleft: ' + str(is_left_chosen) + '\nright: ' + str(right_on) + '\ninterleaved: ' + str(is_interl_chosen)
    cd_2display = '\n\n\n [' + str(attempt_idx) + '] \n AUDIO CHANNELS DICTIONARY' + context + ': ' + beautified_string(channels_dict) + '\n\n' + mode_info + ' \n\n\n'
    logger.info(cd_2display) if (cd_show) else logger.debug(cd_2display)

def assess_discard_policy(options_dictionary):

    #malformed (no numeric, etc: fails entirely)
    with_malformed = 'error (hardcoded)' #just for representational purposes. This parameter
                                         #does not affect anything, shows up in the log only
                                         #to remind the user that, at least at this stage,
                                         #the entire dataset fails if there are malformed data
    def_with_bad_lines = 'warn' #default for long lines - too many fields / error (all dataset fails), skip are other values
    def_with_nans = 'error' #(all dataset fails) default for short lines, Nan in mandatory fields / warn, skip, keep

    on_bad_lines_key = 'on_bad_lines'
    on_nans_key = 'on_nans'
    with_bad_lines = get_optdict_csv_setting(options_dictionary, on_bad_lines_key) if (get_optdict_csv_setting(options_dictionary, on_bad_lines_key)) else def_with_bad_lines
    with_nans = get_optdict_csv_setting(options_dictionary, on_nans_key) if (get_optdict_csv_setting(options_dictionary, on_nans_key)) else def_with_nans
    #with_bad_lines = options_dictionary[on_bad_lines_key] if ((not (options_dictionary is None)) and (on_bad_lines_key in options_dictionary)) else def_with_bad_lines
    #with_nans = options_dictionary[on_nans_key] if ((not (options_dictionary is None)) and (on_nans_key in options_dictionary)) else def_with_nans
    return with_malformed, with_bad_lines, with_nans

def eval_encoding(datafile_path, encoding_choic):
    char_enc = encoding_choic
    if (encoding_choic == 'detected'):
        char_enc = detect_encoding(datafile_path)
        if (char_enc is None):
            char_enc = platform_encoding()
    if (encoding_choic == 'platform'):
        char_enc = platform_encoding()
    return char_enc
