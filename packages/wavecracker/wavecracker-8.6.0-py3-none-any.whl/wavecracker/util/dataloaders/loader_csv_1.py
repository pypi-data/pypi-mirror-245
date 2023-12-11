# v. 6.1.0 231115

import logging
import pandas as pd
import numpy as np

#from file_util import is_text_file
from config_util import get_markers_info, get_csv_info
from common_dataload_util import create_table, eval_encoding, assess_discard_policy, display_headersearch_metadata
from multichannel_util import build_table_def, build_channelsets #, map_loaderout_2old
from float_separators_util import detect_float_separators
from header_detection import guess_csv_header
#from file_util import csv_columns_metadata

def load_raw_csv_1(root_cfg, loading_cfg, attempt_idx, options_dictionary, dfile_path):
    logger = logging.getLogger(__name__)
    loader_type = 'csv'

    #if (not(is_text_file(dfile_path))):
    #    raise Exception(dfile_path + ': not a text file!!')

    #true if the data retrieved are sortable with the PANDAS sorting call visible in the build_channelsets call.
    #as this very loader is written with pandas, this is a TRUE all day
    is_panda_sortable = True
    data = None
    head_cols, x_cols_found, y_cols_found = [], [], []
    channelsets = []
    samples_count_ok = True
    table_def, sort_label = None, None
    #time_vals, signal_vals, num_samples, label_time, label_sign = None, None, 0, None, None
    #label_s_count, label_time, label_sign = get_header_info(root_cfg, loading_cfg)
    time_vals, signal_vals, num_samples = None, None, 0

    c_encoding_choice = get_csv_info(root_cfg, loading_cfg)
    field_sep, float_sep_2bedetected, decimal_separ, thou_separ, comment_prefix, detect_fieldsep, embedded_sep_guesses, additional_sep_guesses = get_markers_info(root_cfg, loading_cfg)
    logger.info('[' + str(attempt_idx) + '] Dataset ingestion attempt #' + str(attempt_idx) + ' ongoing (type: ' + loader_type + ', encoding: ' + c_encoding_choice + ', field separator: ' + str(field_sep) + ', field separator detection: ' + str(detect_fieldsep) + ', numeric separator detection: ' + str(float_sep_2bedetected) + ', comment prefix: ' + str(comment_prefix) + ')')

    # set encoding
    c_encoding = eval_encoding(dfile_path, c_encoding_choice)
    logger.info('[' + str(attempt_idx) + '] Encoding set: ' + c_encoding)

    table_def = create_table(attempt_idx, root_cfg, loading_cfg, options_dictionary)

    rows_to_skip, header_found = 0, False
    logger.debug('[' + str(attempt_idx) + '] Opening dataset: ' + dfile_path)
    # Counting lines until header is found

    rows_to_skip, header_found, x_missed, y_missed, head_cols, x_cols_found, y_cols_found = check_header(attempt_idx, dfile_path, table_def, field_sep, c_encoding, detect_fieldsep, embedded_sep_guesses, additional_sep_guesses)
    #print (str((rows_to_skip, header_found, x_missed, y_missed, head_cols, x_cols_found, y_cols_found)))
    ###########header_found, rows_to_skip = True, 1
    closure_msg_prefix = '[' + str(attempt_idx) + '] Dataset ingestion attempt completed'
    if (not header_found):
        logger.warn('[' + str(attempt_idx) + '] Dataset ingestion attempt completed WITH WARNINGS. Header NOT FOUND in input file, no data can be loaded, check input file)')
    else:
        logger.info('[' + str(attempt_idx) + '] Header FOUND (skipped rows: ' + str(rows_to_skip) + ')')
        skip_rows_val_4_read = rows_to_skip - 1
        #columns_mdata = csv_columns_metadata(dfile_path, c_encoding, field_sep, comment_prefix, skip_rows_val_4_read, decimal_separ)

        if (float_sep_2bedetected):
            logger.info('[' + str(attempt_idx) + '] Numeric separators detection ongoing ..')
            float_sep_detected, det_decimal_sep, det_thous_sep = detect_float_separators(attempt_idx, dfile_path, c_encoding, field_sep, comment_prefix, skip_rows_val_4_read + 1)
            if (float_sep_detected):
                decimal_separ, thou_separ = det_decimal_sep, det_thous_sep
        logger.info('[' + str(attempt_idx) + '] Decimal separator: ' + str(decimal_separ) + ', thousands separator: ' + str(thou_separ))

        display_headersearch_metadata(attempt_idx, head_cols, x_cols_found, y_cols_found)
        all_cols_found = (x_missed + y_missed) == 0
        if (not all_cols_found):
            logger.warn('[' + str(attempt_idx) + '] INCOMPLETE HEADER, partial results expected (missing axes count: {x: ' + str(x_missed) + ', y: ' + str(y_missed) + '})')

        with_malformed, with_bad_lines, with_nans  = assess_discard_policy(options_dictionary)
        logger.info('[' + str(attempt_idx) + '] Discard policies in place: {malformed: ' + with_malformed + ', on bad lines: ' + with_bad_lines + ', on NaN values: ' + with_nans + '}')

        #print (' \n\n\n decimal_separ= ' + str(decimal_separ) + ' \n\n\n ')
        # ATTENZIONE separator e decimal_separator DEVONO ESSERE VALORIZZATE, con None non funziona
        try:
            data = pd.read_csv(dfile_path, encoding=c_encoding, delimiter=field_sep, comment=comment_prefix, skiprows=skip_rows_val_4_read, decimal=decimal_separ, thousands=thou_separ, on_bad_lines = with_bad_lines)
            #print('XPANDA: ' + str(type(data['Time(s)'][0])))
        except Exception as e:
            logger.warning('[' + str(attempt_idx) + '] read_csv FAILED (' + str(e) + '), now trying again WITHOUT on_bad_lines argument')
            data = pd.read_csv(dfile_path, encoding=c_encoding, delimiter=field_sep, comment=comment_prefix, skiprows=skip_rows_val_4_read, decimal=decimal_separ, thousands=thou_separ)

        #mandatory_nan_fields = [label_time, label_sign]
        mandatory_nan_fields = x_cols_found + [i for i in y_cols_found if i not in x_cols_found]
        data = process_nans(attempt_idx, data, mandatory_nan_fields, with_nans)

        min_num_samples, max_num_samples, samples_count_ok, channelsets = build_channelsets(attempt_idx, table_def, x_cols_found, y_cols_found, None, data, is_panda_sortable, None)
        logger.debug('[' + str(attempt_idx) + '] Num. of samples: ' + str(min_num_samples))
        if (not (min_num_samples == max_num_samples)):
            logger.warning('[' + str(attempt_idx) + '] Num. of samples seems different across columns, min./max: ' + str(min_num_samples)) + '/' + str(max_num_samples)

    logger.debug('\n\n[' + str(attempt_idx) + '] CSV cs (len: ' + str(len(channelsets)) + ') before leaving loader: ' + str(channelsets))
    #return num_samples, samples_count_ok, channelsets
    return samples_count_ok, channelsets

def check_header(attempt_idx, dfile_path, table_def, field_sep_in, df_encoding, guess_header, embedded_sep_guesses, additional_sep_guesses):
    logger = logging.getLogger(__name__)
    rows_to_skip = 0
    header_found = False
    x_missed, y_missed = 0, 0
    header_columns, x_columns_found, y_columns_found = [], [], []

    #print(table_def)
    # DISTINCT axes names I am looking for
    required_x_axes = {field['name'] for field in table_def['fields'] if 'x_ref' not in field}
    required_y_axes = {field['name'] for field in table_def['fields'] if 'x_ref' in field}
    num_x_to_find = len(required_x_axes)
    num_y_to_find = len(required_y_axes)
    #logger.info('[' + str(attempt_idx) + '] Searching x axes columns (' + str(num_x_to_find) + '): ' + ', '.join(required_x_axes))
    #logger.info('[' + str(attempt_idx) + '] Searching y axes columns (' + str(num_y_to_find) + '): ' + ', '.join(required_y_axes))

    logger.info('[' + str(attempt_idx) + '] Searching for header [x-columns: ' + ', '.join(required_x_axes) + '; y-columns: ' + ', '.join(required_y_axes) + '] ...')

    field_sep = field_sep_in

    guessed_line = None
    if (guess_header): # note this routine actually guesses ALSO header position, but I use it ONLY for separator.
        logger.info('[' + str(attempt_idx) + '] Field separator detection ongoing...')
        fsep_list = embedded_sep_guesses + additional_sep_guesses
        h_guesses = guess_csv_header(attempt_idx, dfile_path, df_encoding, fsep_list, required_x_axes, required_y_axes)
        logger.debug('[' + str(attempt_idx) + '] Header guesses: ' + str(h_guesses))
        num_hguesses = len(h_guesses)
        if (num_hguesses > 0):
            #i pick first guess
            field_sep, guessed_line = h_guesses[0]
            logger.info('[' + str(attempt_idx) + '] Detected field separator: ' + field_sep)
        else:
            logger.info('[' + str(attempt_idx) + '] No field separator detection made. Going with the configured field separator.')

    header_columns = []
    x_columns_found = []
    y_columns_found = []
    with open(dfile_path, 'r', encoding=df_encoding) as in_file:
        for num, data_line_d in enumerate(in_file, 1):
            data_line = data_line_d.strip() #fondamentale togliere l'a capo finale!!! salta tutto diversamente!!
            #logger.warning('[' + str(attempt_idx) + '] \n\n >' + data_line)
            x_axes_found = False
            y_axes_found = False
            field_sep_found = field_sep in data_line
            if (field_sep_found):
                header_columns_candidates = data_line.split(field_sep)
                #x_axes_found =  any(x_ax in data_line for x_ax in required_x_axes)
                #y_axes_found = any(y_ax in data_line for y_ax in required_y_axes)
                x_axes_found =  any(x_ax in header_columns_candidates for x_ax in required_x_axes)
                y_axes_found = any(y_ax in header_columns_candidates for y_ax in required_y_axes)
                headers_and_sep_found = x_axes_found and y_axes_found
                if (headers_and_sep_found):
                    header_columns = header_columns_candidates #data_line.split(field_sep)
                    no_dup_header_fields = not (len(header_columns) != len(set(header_columns)))
                    if (no_dup_header_fields):
                        header_found = True
                        rows_to_skip = num
                        logger.debug('[' + str(attempt_idx) + '] line #' + str(num) + ': found header !')
                        x_columns_found = [field_name for field_name in header_columns if field_name in required_x_axes]
                        y_columns_found = [field_name for field_name in header_columns if field_name in required_y_axes]
                        #logger.warning('[' + str(attempt_idx) + '] ')
                        break
                    else:
                        logger.warning('[' + str(attempt_idx) + '] Duplicate fields in header candidate [line: ' + str(num) + '; fields: ' + ', '.join(header_columns) + ']')
    x_missed = len([field_name for field_name in required_x_axes if (not (field_name in header_columns))])
    y_missed = len([field_name for field_name in required_y_axes if (not (field_name in header_columns))])
    logger.debug('[' + str(attempt_idx) + '] Missed x, y axes: ' + str(x_missed) + ', ' + str(y_missed))

    if (guessed_line):
        if (not (guessed_line == rows_to_skip)):
            logger.warn('[' + str(attempt_idx) + '] Possible wrong field separator guess, guessed/evaluated line # are different: ' + str(guessed_line) + '/' + str(rows_to_skip))

    return rows_to_skip, header_found, x_missed, y_missed, header_columns, x_columns_found, y_columns_found

def process_nans(attempt_idx, data_raw, mandatory_fields, with_nans):
    logger = logging.getLogger(__name__)
    dataframe = data_raw
    num_samples_raw = len(data_raw)                   # Number of samples RAW, i.e. including NaNs ('short rows', rows with less fields)
    logger.debug('[' + str(attempt_idx) + '] Raw data loaded (raw samples: ' + str(num_samples_raw) + ')')
    #Process NaNs
    logger.debug('[' + str(attempt_idx) + '] Processing NaNs on fields: ' + str(mandatory_fields))
    data_without_nans = data_raw.dropna(subset=mandatory_fields)
    rows_with_nans = num_samples_raw - len(data_without_nans)
    logger.info('[' + str(attempt_idx) + '] Rows with NaN values: ' + str(rows_with_nans) + ' (fields checked: ' + ', '.join(mandatory_fields) + ')')
    if (rows_with_nans > 0):
        if (with_nans == 'error'):
            raise Exception('Found rows with NaN values (' + str(rows_with_nans) + '), check data !')
        if (with_nans == 'skip'):
            dataframe = data_without_nans
            logger.debug('[' + str(attempt_idx) + '] Rows with NaN values are being skipped: ' + str(rows_with_nans))
        if (with_nans == 'warn'):
            dataframe = data_without_nans
            logger.warning('[' + str(attempt_idx) + '] Found rows with NaN values: ' + str(rows_with_nans))
    return dataframe

