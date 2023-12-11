# v. 5.5.0 231114

import os
import sys
import pathlib
import pandas as pd
import chardet
#import datetime
from config_util import get_ftdatafile_info
from common_util import get_formatted_tstamp
import logging

import pandas as pd

#def csv_columns_metadata(dfile_path, c_encoding, field_sep, comment_prefix, rows_to_skip, decimal_separ):
#    logger = logging.getLogger(__name__)
#    columns_mdata = None
#    try:
#        data_temp = pd.read_csv(dfile_path, encoding=c_encoding, delimiter=field_sep, comment=comment_prefix, skiprows=rows_to_skip, decimal=decimal_separ, nrows=1)
#        columns_mdata = data_temp.columns
#    except Exception as e:
#        columns_mdata = None
#        logger.warning('Minor error while retrieving column metadata: ' + str(e))
#    return columns_mdata

#tentata per il problema noto PYTHON-0015, ma non funziona, visto che ha attribuito un encoding ad un eseguibile ....
#def is_text_file(file_path):
#    logger = logging.getLogger(__name__)
#    with open(file_path, 'rb') as f:
#        result = chardet.detect(f.read(1024))  # Read a chunk to detect the character encoding
#    logger.error('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ' + str(result['encoding']))
#    return result['encoding'] is not None

def get_file_basename(fname):
    return os.path.basename(fname)

def get_file_basename_and_ext(fname):
    basename_splitted = os.path.splitext(get_file_basename(fname))
    f_basename_wo_ext, f_extension = basename_splitted[0], basename_splitted[1][1:]
    f_extension = f_extension if (len(f_extension) > 0) else None
    return f_basename_wo_ext, f_extension

def save_ft_data(datafile_name, iter_token, config_hnd, out_directory, out_overwrite, x_axis_values_list, y_axis_values_list, y_headers_list, data_out_mode):
    logger = logging.getLogger(__name__)
    num_plots_saved = 0
    all_option = 'all'
    ft_2save = (data_out_mode in ['ft', all_option])   #'none', 'ft', 'all'
    anything_2_save = ft_2save
    if (anything_2_save):
        if (ft_2save):
            x_col_name, y_col_name, out_encoding, datafile_ext, index_field, sep, dec_sep, floatformat, fname_suffix, tstamp_suff_format = get_ftdatafile_info(config_hnd)
            num_plots_saved = save_out_data(datafile_name, iter_token, fname_suffix, 'Fourier Transform', config_hnd, out_directory, out_overwrite, x_axis_values_list, y_axis_values_list, y_headers_list, x_col_name, y_col_name, out_encoding, datafile_ext, index_field, sep, dec_sep, floatformat, tstamp_suff_format)
    else:
        logger.info('No data saved (per user request)')
    return num_plots_saved

def check_critical_files(fileslist):
    rc = True
    files_missing = []
    for f in fileslist:
        if (not os.path.exists(f)):
            #print('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '][CRITICAL] MISSING: ' + f)
            files_missing.append(f)
    rc = (len(files_missing) == 0)
    return rc, files_missing

def save_out_data(datafile_name, iter_token, fname_suffix, out_desc, config_hnd, out_directory, out_overwrite, x_axis_values_list, y_axis_values_list, y_headers_list, x_col_name, y_col_name, out_encoding, out_extension, index_field, sep, dec_sep, floatformat, tstamp_suff_fmt):
    logger = logging.getLogger(__name__)
    num_plots = 0
    #import time
    #time.sleep(20)
    #if (do_parall):
    #    logger.info(out_desc + ': output data being saved in background ...')
    #   x_axis_values, y_axis_values
    num_plots = len(y_axis_values_list)
    #print('>>>>>>>>>>>>>> PRE-PRE  ' + str(num_plots))
    datafile_name_wo_ext, _ = get_file_basename_and_ext(datafile_name)
    datafile_basename = datafile_name_wo_ext + (iter_token if (iter_token) else '')
    tstamp_token = '' if (tstamp_suff_fmt is None) else ('-' + get_formatted_tstamp(tstamp_suff_fmt))
    out_datafile = out_directory + '/' + datafile_basename + '-' + fname_suffix + tstamp_token + '.' + out_extension
    ftdata_2_be_written = (out_overwrite or (not os.path.exists(out_datafile)))
    if (ftdata_2_be_written):
        index_val = (not (index_field is None)) and (len(index_field) > 0)
        if (os.path.exists(out_directory)):
            # Save the data
            x_axis_values = x_axis_values_list[0]
            #if (num_plots < 2):
            #    ft_data = pd.DataFrame({x_col_name: x_axis_values, y_col_name + '(' + y_headers_list[0] + ')': y_axis_values_list[0]})
            #    #logger.debug(out_desc + ' data frame created (single plot)')
            #else:
            ft_data = {x_col_name: x_axis_values}
            ft_data.update({y_col_name + '(' + y_signal_label + ')': signal_data for y_signal_label, signal_data in zip(y_headers_list, y_axis_values_list)})
            # Create a DataFrame
            ft_data = pd.DataFrame(ft_data)
            # Save the DataFrame to a CSV file
            #logger.debug(out_desc + ' data frame created (plots: ' + str(num_plots) + ')')
            ft_data.to_csv(out_datafile, index=index_val, index_label=index_field, sep=sep, decimal=dec_sep, float_format=floatformat, encoding=out_encoding)
            logger.info(out_desc + ' output data saved (plots: ' + str(num_plots) + ', ' + out_datafile + ', encoding: ' + out_encoding + ')')
        else:
            logger.error(out_desc + ' output data cannot be saved, output directory (' + out_directory + ') does not exist')
    else:
        logger.info(out_desc +' output data not saved (cannot overwrite ' + out_datafile + ')')
    return num_plots

def platform_encoding():
    return sys.getdefaultencoding()

def detect_encoding(file_path):
    encoding = None
    with open(file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
        encoding = result['encoding']
    return encoding

def create_files_list(input_dir_or_file, file_extensions):
    logger = logging.getLogger(__name__)
    num_files=0
    file_list = []
    f_exists, is_file, is_dir = get_fs_objnature(input_dir_or_file)

    if (f_exists):
        logger.info('Input data path: ' + input_dir_or_file)
        if (is_dir):
            logger.info('File list creation ongoing ...')
            #file_extensions = file_extensions_str.split(',')
            files_root_dir = pathlib.Path(input_dir_or_file)

            if (file_extensions is None):
                allfiles_list = list(files_root_dir.rglob('*'))
                file_list = file_list + allfiles_list
                logger.info('Added all files (' + str(len(allfiles_list)) + ')')
            else:
                for cur_ext in file_extensions:
                    cur_ext_list = list(files_root_dir.rglob('*.' + cur_ext))
                    file_list = file_list + cur_ext_list
                    logger.info('Added *.' + cur_ext + ' files (' + str(len(cur_ext_list)) + ')')

            #for item in list(files_root_dir.rglob("*.jpg")) + list(files_root_dir.rglob("*.jpeg")):
            #for item in file_list:
            #    num_files=num_files+1
        if (is_file):
            #num_files=num_files+1
            file_list.append(input_dir_or_file)

        num_files = len(file_list)
        if (num_files > 0):
            logger.info('File list created (items: ' + str(num_files) + ')')
    else:
        logger.error('FILE NOT FOUND: ' + input_dir_or_file)
    return file_list, num_files

def get_fs_objnature(path):
    logger = logging.getLogger(__name__)
    is_dir = False
    is_file = False
    logger.debug('Analyzing: ' + path)
    f_exists = os.path.exists(path)
    if (f_exists):
        if os.path.isfile(path):
            is_file = True
        elif os.path.isdir(path):
            is_dir = True
        else:
            logger.debug('This object is not a file, neither a directory: ' + path)
    return f_exists, is_file, is_dir