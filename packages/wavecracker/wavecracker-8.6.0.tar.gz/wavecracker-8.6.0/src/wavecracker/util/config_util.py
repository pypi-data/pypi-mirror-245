# v. 8.6.0 231210

import logging
import yaml
import re

from common_util import beautified_string

def get_config_hnd(exc_if_not_loaded, desc, conf_file_path):
    logger = logging.getLogger(__name__)
    logger.debug('Loading configuration (' + desc + ', from: ' + conf_file_path + ') ....')
    config = None
    try:
        with open(conf_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        logger.debug('Configuration loaded (' + desc + ', from: ' + conf_file_path + '): \n' + beautified_string(config))
    except Exception as e:
        strerr = 'Configuration file not found (role: ' + desc + ', path: ' + conf_file_path + '): ' + str(e)
        if (exc_if_not_loaded):
            raise Exception(strerr)
        else:
            logger.warn(strerr)
    return config

def get_loading_csv_settings(loading_config):
    csv_load_key = 'csv'
    load_csv_settings = loading_config[csv_load_key] if (loading_config and (csv_load_key in loading_config)) else None
    return load_csv_settings

def get_loading_csv_setting(loading_config, skey):
    load_csv_settings = get_loading_csv_settings(loading_config)
    ret_val = load_csv_settings[skey] if (load_csv_settings and (skey in load_csv_settings)) else None
    return ret_val

def get_tabledef_id_override(loading_config):
    td_key = 'table_def'
    return get_loading_csv_setting(loading_config, td_key)

def resolve_tabledef_id(config, loading_config, table_def_override_cmd_line):
    logger = logging.getLogger(__name__)
    tdef_id_override = get_tabledef_id_override(loading_config)
    #print ('xxxxxxxxxxxxxxxxxxxx tdef_id_override dalla conf: ' + (tdef_id_override if tdef_id_override else 'None'))
    if (not (tdef_id_override is None)):
        logger.debug('overriding default table_def id with configured one: ' + tdef_id_override)
        return tdef_id_override
    else:
        td_key = 'table_def'
        if (table_def_override_cmd_line):
            table_def = table_def_override_cmd_line
        else:
            default_csv_params = get_default_csv_params(config)
            if (config and default_csv_params and (td_key in default_csv_params)):
                table_def = default_csv_params[td_key]
                logger.debug('table def id: ' + table_def)
            else:
                raise Exception('Table ID not resolved (check configuration)')
        return table_def

def get_audio_constants(config):
    audio_gen_cfg = get_audio_gen_config(config)
    x_label = audio_gen_cfg['xlabel']
    x_filetoken = audio_gen_cfg['x_filetoken'] if ('x_filetoken' in audio_gen_cfg) else 't'
    return x_label, x_filetoken

def get_qqplot_params(config):
    plots_config = get_plots_config(config)
    qq_config = plots_config['qq_plot']
    bgcolor = qq_config.get('bgcolor')
    plot_title_base = qq_config.get('title')
    qq_type = qq_config.get('distr_type')
    orig_xlabel = qq_config.get('xlabel')
    def_ylabel = qq_config.get('ylabel') if 'ylabel' in qq_config else None
    orig_grid = qq_config.get('grid')
    orig_yscale = qq_config.get('yscale')
    comp_linewidth = qq_config.get('comp_linewidth')
    comp_color = qq_config.get('comp_color')
    sign_color = qq_config.get('sign_color')
    marker = qq_config.get('marker')
    markerface_color = qq_config.get('markerface_color')
    markersize = qq_config.get('markersize')
    shape_param = qq_config.get('sp_shape')
    scale_param = qq_config.get('sp_scale')
    return bgcolor, plot_title_base, qq_type, orig_xlabel, def_ylabel, orig_grid, orig_yscale, comp_linewidth, comp_color, sign_color, marker, markerface_color, markersize, shape_param, scale_param

def get_badplot_params(config):
    #base_msg, with_err_msg, max_cols, max_len, x_pos, y_pos, x_text, y_text, fcolor, fshrink, mut_scale =
    #'RENDERING ERROR', True, 40, 255, 0.5, 0.5, 0.5, 0.5, 'red', 0.05, 40
    plots_config = get_plots_config(config)
    bp_config = plots_config['plot_error']
    base_msg = bp_config.get('base_message')
    with_err_msg = bp_config.get('with_err_msg')
    max_cols = bp_config.get('max_cols')
    max_len = bp_config.get('max_len')
    x_pos = bp_config.get('x_pos')
    y_pos = bp_config.get('y_pos')
    x_text = bp_config.get('x_text')
    y_text = bp_config.get('y_text')
    fcolor = bp_config.get('color')
    fshrink = bp_config.get('shrink')
    mut_scale = bp_config.get('mut_scale')
    return base_msg, with_err_msg, max_cols, max_len, x_pos, y_pos, x_text, y_text, fcolor, fshrink, mut_scale

def get_loader_override(loading_config):
    loader_key = 'loader'
    load_fun_ovname = loading_config.get(loader_key) if ((not (loading_config is None)) and (loader_key in loading_config)) else None
    return load_fun_ovname

def get_loader_by_ext(root_config, file_extension):
    load_fun_name = None
    cfg_input_data = get_input_data_config(root_config)
    def_loader_fun = cfg_input_data.get('loader')
    ext_2_loaders_map = cfg_input_data['loaders_map']
    extension_lcase = None if (file_extension is None) else file_extension.lower()
    load_fun_name = ext_2_loaders_map.get(extension_lcase) if ((not (extension_lcase is None)) and extension_lcase in ext_2_loaders_map) else def_loader_fun
    #function_mapping = {
    #    'csv': load_raw_csv,
    #    'txt': load_raw_csv,
    #    'mp3': load_raw_mp3,
    #    'mp4': load_raw_mp4,
    #}
    #loader_function = function_mapping.get(extension_lcase, def_extension)
    return load_fun_name

def get_load_prof_prefix():
    return 'profile_'

def get_load_profiles_rootname():
    return 'loading_profiles'

def load_profiles_rcompact(config):
    logger = logging.getLogger(__name__)
    loading_profs_key = get_load_profiles_rootname()
    input_data_config = get_input_data_config(config)
    profilepattern_str = '^' + get_load_prof_prefix() + '(\d+)$'
    logger.debug('Loading profile search pattern: ' + profilepattern_str)
    profpattern = re.compile(profilepattern_str)
    numeric_suffixes = [int(profpattern.search(key).group(1)) for key in input_data_config.get(loading_profs_key, {}).keys() if profpattern.search(key)]
    num_profiles = len(numeric_suffixes)
    # Check if the sequence is compact without gaps
    return num_profiles, ((num_profiles < 2) or all(y - x == 1 for x, y in zip(numeric_suffixes, numeric_suffixes[1:])))

def get_loading_config(config, idx):
    logger = logging.getLogger(__name__)
    profile_config = None
    loading_profs_key = get_load_profiles_rootname()
    keystr = get_load_prof_prefix() + str(idx)
    input_data_config = get_input_data_config(config)
    #sequence_ok = load_profiles_rcompact(input_data_config, loading_profs_key)
    #logger.debug('Loading Profile Sequence IS COMPACT: ' + str(sequence_ok))
    profiles_exist = loading_profs_key in input_data_config
    #if (not profiles_exist):
    #    raise Exception('LOADING PROFILES NOT FOUND, no processing can take place. Check configuration')
    keyIsPresent = profiles_exist and (keystr in input_data_config[loading_profs_key])
    if (keyIsPresent):
        profile_config = input_data_config[loading_profs_key][keystr]
    #if (idx < 2) and (not keyIsPresent):
    #    raise Exception('LOADING PROFILE #' + str(idx) + ' NOT FOUND [parent section (' + loading_profs_key + ') present: ' + str(profiles_exist) + '], no processing can take place. Check configuration')
    logger.debug('get_loading_config: ' + keystr + ' is present: ' + str(keyIsPresent))
    return keyIsPresent, profile_config

def get_ftdatafile_info(config):
    out_config = get_output_config(config)
    ftdata_config = out_config['ft_data']
    x_col_name = ftdata_config['xlabel']
    y_col_name = ftdata_config['ylabel']
    ft_datafile_encod = ftdata_config['encoding']
    ft_datafile_ext = ftdata_config['ext']
    indx_key = 'index_field'
    index_field_name = ftdata_config[indx_key] if (indx_key in ftdata_config) else None
    fname_suffix = ftdata_config.get('filename_suffix')
    tstampfmt_key = 'timestamp_suffix'
    tstamp_suffix_format = ftdata_config[tstampfmt_key] if (tstampfmt_key in ftdata_config) else None
    sep = ftdata_config['separator']
    dec_sep = ftdata_config['decimal_separator']
    #thou_sep_key = 'thoudsands_separator' - not supported in output
    #thou_sep = ftdata_config[thou_sep_key] if (thou_sep_key in ftdata_config) else None
    floatformat_key = 'float_format'
    floatformat = ftdata_config[floatformat_key] if (floatformat_key in ftdata_config) else None
    return x_col_name, y_col_name, ft_datafile_encod, ft_datafile_ext, index_field_name, sep, dec_sep, floatformat, fname_suffix, tstamp_suffix_format

#def eval_loading_cfg_param(loading_cfg, group_key, item_key, def_value):
#    logger = logging.getLogger(__name__)
#    ret_val = def_value
#    if (not (loading_cfg is None)) and (group_key in loading_cfg) and (item_key in loading_cfg[group_key]):
#        ret_val = loading_cfg[group_key][item_key]
#    logger.debug('loading_config[' + group_key + '][' + item_key + '] resolved: ' + ret_val)
#    return ret_val

def eval_loading_csv_param(loading_cfg, group_key, item_key, def_value):
    logger = logging.getLogger(__name__)
    loading_csv_settings = get_loading_csv_settings(loading_cfg)
    ret_val = def_value
    if (group_key):
        group_config = loading_csv_settings[group_key] if ((loading_csv_settings) and (group_key in loading_csv_settings)) else None
        if (group_config and (item_key in group_config)):
            ret_val = group_config[item_key]
    else:
        if (loading_csv_settings and (item_key in loading_csv_settings)):
            ret_val = loading_csv_settings[item_key]
    logger.debug('loading_config csv[' + (group_key if (group_key) else '-') + '][' + item_key + '] resolved: ' + str(ret_val))
    return ret_val

def get_default_csv_params(config):
    input_data_config = get_input_data_config(config)
    csv_key = 'csv'
    def_csv_config = input_data_config[csv_key]
    return def_csv_config

def get_csv_info(config, loading_config):
    def_csv_config = get_default_csv_params(config)
    encoding_key = 'encoding'
    def_encoding = def_csv_config.get(encoding_key)
    c_charencoding = eval_loading_csv_param(loading_config, None, encoding_key, def_encoding)
    return c_charencoding
    
    def_detect_float_seps = def_csv_config.get(floatsep_det_key)
    detect_float_seps = eval_loading_csv_param(loading_config, None, floatsep_det_key, def_detect_float_seps)
    detect_float_seps

#def get_markers_grp_key():
#    return 'markeXrs'

def get_markers_info(config, loading_config):
    default_csv_config = get_default_csv_params(config)
    markers_key = 'markers' #get_markers_grp_key()
    separator_key = 'separator'
    floatsep_det_key = 'detect_float_separators'
    dec_separator_key = 'decimal_separator'
    thou_separator_key = 'thousands_separator'
    comment_key = 'comment'
    header_det_key = 'detect_header'
    fieldsep_guesses_key = 'field_sep_guesses'
    embedded_sep_guesses = [' ', '\t']

    def_markers_config = default_csv_config[markers_key] if markers_key in default_csv_config else None
    def_separator, def_dec_separator, def_thou_separator, def_comment = None, None, None, None
    if (def_markers_config):
        def_separator = def_markers_config.get(separator_key) if separator_key in def_markers_config else None
        def_detect_numeric_seps = def_markers_config.get(floatsep_det_key) if floatsep_det_key in def_markers_config else False
        def_dec_separator = def_markers_config.get(dec_separator_key) if dec_separator_key in def_markers_config else None
        def_thou_separator = def_markers_config.get(thou_separator_key) if thou_separator_key in def_markers_config else None
        def_comment = def_markers_config.get(comment_key) if comment_key in def_markers_config else None
        def_detect_header = def_markers_config.get(header_det_key) if header_det_key in def_markers_config else False
        def_addsep_guesses_str = def_markers_config.get(fieldsep_guesses_key) if fieldsep_guesses_key in def_markers_config else None

    separator = eval_loading_csv_param(loading_config, markers_key, separator_key, def_separator)
    detect_numeric_seps = eval_loading_csv_param(loading_config, markers_key, floatsep_det_key, def_detect_numeric_seps)
    dec_separator = eval_loading_csv_param(loading_config, markers_key, dec_separator_key, def_dec_separator)
    thou_separator = eval_loading_csv_param(loading_config, markers_key, thou_separator_key, def_thou_separator)
    comment = eval_loading_csv_param(loading_config, markers_key, comment_key, def_comment)
    detect_header = eval_loading_csv_param(loading_config, markers_key, header_det_key, def_detect_header)

    addsep_guesses_str = eval_loading_csv_param(loading_config, markers_key, fieldsep_guesses_key, def_addsep_guesses_str)
    addsep_guesses = [ichar for ichar in addsep_guesses_str] if (addsep_guesses_str) else []
    return separator, detect_numeric_seps, dec_separator, thou_separator, comment, detect_header, embedded_sep_guesses, addsep_guesses


def get_rainbow_colors(config):
    plots_config = get_plots_config(config)
    rainbow_str = plots_config.get('rainbow')
    return rainbow_str

#clean up empty subplots
def get_emptysubplots_params(config):
    empty_wspace, empty_hspace = 0, 0
    plots_config = get_plots_config(config)
    emptysb_config = plots_config.get('empty_subplots')
    empty_wspace = emptysb_config.get('wspace')
    empty_hspace = emptysb_config.get('hspace')
    return empty_wspace, empty_hspace

def get_common_plots_params(config):
    plots_config = get_plots_config(config)
    wind_title = plots_config.get('window_title')
    bgcolor = plots_config.get('bgcolor')
    return wind_title, bgcolor

def get_1tab_ui_plots_params(config):
    plots_config = get_plots_config(config)
    old_ui_config = plots_config.get('ui_1tab')
    max_rows = old_ui_config.get('max_rows')
    max_cols = old_ui_config.get('max_columns')
    cellspan_config = old_ui_config.get('cellspan')
    h_cell_span = cellspan_config.get('height')
    w_cell_span = cellspan_config.get('width')
    figsz_config = old_ui_config.get('figsize')
    figsz_w = figsz_config.get('width')
    figsz_h = figsz_config.get('height')
    gridsp_config = old_ui_config.get('gridspec')
    gridspec_hs = gridsp_config.get('hspace')
    gridspec_ws = gridsp_config.get('wspace')
    return max_rows, max_cols, h_cell_span, w_cell_span, figsz_w, figsz_h, gridspec_hs, gridspec_ws

def get_mtab_ui_plots_params(config):
    plots_config = get_plots_config(config)
    mtui_config = plots_config.get('ui_multitab')
    anonym_tab_pfix = mtui_config.get('anon_tab_prefix')
    max_rows = mtui_config.get('max_rows')
    max_cols = mtui_config.get('max_columns')
    max_plotsxtab = mtui_config.get('max_plots_per_tab')
    expand = mtui_config.get('expand')
    tab_expand = mtui_config.get('tab_expand')
    fill = mtui_config.get('fill')
    tab_fill = mtui_config.get('tab_fill')
    tab_side = mtui_config.get('tab_side')
    tab_dpi = mtui_config.get('dpi')
    figsz_config = mtui_config.get('figsize')
    figsz_w = figsz_config.get('width')
    figsz_h = figsz_config.get('height')
    gridsp_config = mtui_config.get('gridspec')
    gridspec_hs = gridsp_config.get('hspace')
    #gridspec_ws = gridsp_config.get('wspace')
    return anonym_tab_pfix, max_rows, max_cols, max_plotsxtab, expand, tab_expand, fill, tab_fill, tab_side, tab_dpi, figsz_w, figsz_h, gridspec_hs #, gridspec_ws

def get_3dspectrogramplot_params(config):
    plots_config = get_plots_config(config)
    spec3_config = plots_config.get('spectrogram_3d')
    spec3_title = spec3_config.get('title')
    spec3_dbmlt = spec3_config.get('db_multiplier')
    spec3_ylabel = spec3_config.get('ylabel')
    spec3_zlabel = spec3_config.get('zlabel')
    spec3_colormap = spec3_config.get('color_map')
    spec3_edgecol = spec3_config.get('edgecolors')
    sp3dbgcolor = spec3_config.get('bgcolor')
    return spec3_title, spec3_dbmlt, spec3_ylabel, spec3_zlabel, spec3_colormap, spec3_edgecol, sp3dbgcolor

def get_spectrogramplot_params(config):
    plots_config = get_plots_config(config)
    spec_config = plots_config.get('spectrogram')
    spec_title = spec_config.get('title')
    #spec_xlabel = spec_config.get('xlabel')
    spec_ylabel = spec_config.get('ylabel')
    spec_colorbar_label = spec_config.get('colorbarlabel')
    spec_yscale = spec_config.get('yscale')
    spec_grid = spec_config.get('grid')
    spec_color_map = spec_config.get('color_map')
    return spec_title, spec_ylabel, spec_colorbar_label, spec_yscale, spec_grid, spec_color_map

def get_envelope_params(config): # 'red', 'envelope', 1
    original_config = get_origplot_confroot(config)
    env_config = original_config.get('envelope')
    env_color = env_config.get('color')
    env_label = env_config.get('label')
    env_lwidth = env_config.get('linewidth')
    return env_color, env_label, env_lwidth

def get_sigfilt_params(config):
    original_config = get_origplot_confroot(config)
    filt_config = original_config.get('filtered_signal')
    sig_filtered_color = filt_config.get('color')
    sig_filtered_linestyle = filt_config.get('linestyle')
    sig_filtered_linewidth = filt_config.get('linewidth')
    sig_filt_label = filt_config.get('label')
    return sig_filtered_color, sig_filtered_linestyle, sig_filtered_linewidth, sig_filt_label

def get_origplot_confroot(config):
    plots_config = get_plots_config(config)
    original_config = plots_config.get('original')
    return original_config

def get_origsignalplot_title(config):
    original_config = get_origplot_confroot(config)
    orig_title = original_config.get('title')
    orig_type_label = original_config.get('type_label')
    return orig_type_label, orig_title

def get_instfreqplot_params(config):
    freqpl_config = get_freqplots_config(config)
    instfrq_config = freqpl_config['inst_freq']
    orig_bgcolor = instfrq_config.get('bgcolor')
    orig_title = instfrq_config.get('title')
    orig_ylabel = instfrq_config.get('ylabel')
    orig_yscale = instfrq_config.get('yscale')
    orig_grid = instfrq_config.get('grid')
    color = instfrq_config.get('color')
    sig_color = instfrq_config.get('sig_color')
    orig_lwidth = instfrq_config.get('linewidth')
    sig_linewidth = instfrq_config.get('sig_linewidth')
    sig_linestyle = instfrq_config.get('sig_linestyle')
    sig_ylabel = instfrq_config.get('sig_ylabel')
    return orig_title, orig_ylabel, orig_bgcolor, orig_yscale, orig_grid, sig_color, color, orig_lwidth, sig_linestyle, sig_linewidth, sig_ylabel

def get_origplot_params(config):
    original_config = get_origplot_confroot(config)
    orig_bgcolor = original_config.get('bgcolor')
    #orig_title = original_config.get('title')
    #orig_xlabel = original_config.get('xlabel')
    #orig_ylabel = original_config.get('ylabel')
    orig_yscale = original_config.get('yscale')
    orig_grid = original_config.get('grid')
    orig_color = original_config.get('color')
    orig_lwidth = original_config.get('linewidth')
    orig_label = original_config.get('label')
    #return orig_bgcolor, orig_title, orig_xlabel, orig_ylabel, orig_yscale, orig_grid, orig_color, orig_lwidth, orig_label
    return orig_bgcolor, orig_yscale, orig_grid, orig_color, orig_lwidth, orig_label

def get_freq_xgrain(config):
    ft_config = get_freqplots_config(config)
    xgrain = ft_config.get('frequency_grain')
    return xgrain

def get_wvletcalc_params(config):
    proc_config = get_processing_config(config)
    wv_config = proc_config['wavelet_transform']
    scale_range_low = wv_config['scale_low']
    scale_range_max = wv_config['scale_high']
    wavelet_type = wv_config['wvtype']
    return scale_range_low, scale_range_max, wavelet_type

def get_psdcalc_params(config):
    proc_config = get_processing_config(config)
    psd_config = proc_config['psd']
    scaling_set = psd_config.get('scaling')
    is_onesided = psd_config.get('onesided')
    return scaling_set, is_onesided

def get_psdplot_params(config):
    psd_config = get_psdplot_config(config)
    psd_title = psd_config.get('title')
    psd_xlabel = psd_config.get('xlabel')
    psd_ylabel = psd_config.get('ylabel')
    psd_grid_reqd = psd_config.get('grid')
    psd_yscale = psd_config.get('yscale')
    psd_color = psd_config.get('color')
    psd_bgcolor = psd_config.get('bgcolor')
    psd_linewidth = psd_config.get('linewidth')
    return psd_title, psd_xlabel, psd_ylabel, psd_grid_reqd, psd_yscale, psd_color, psd_bgcolor, psd_linewidth

def get_ftphaseplot_params(config):
    freqpl_config = get_freqplots_config(config)
    phasepl_config = freqpl_config['ft_phase']
    ph_title = phasepl_config.get('title')
    ph_xlabel = phasepl_config.get('xlabel')
    ph_ylabel = phasepl_config.get('ylabel')
    ph_grid_reqd = phasepl_config.get('grid')
    ph_yscale = phasepl_config.get('yscale')
    ph_color = phasepl_config.get('color')
    ph_bgcolor = phasepl_config.get('bgcolor')
    ph_linewidth = phasepl_config.get('linewidth')
    return ph_title, ph_xlabel, ph_ylabel, ph_grid_reqd, ph_yscale, ph_color, ph_bgcolor, ph_linewidth


def get_wvletplot_params(config):
    # 1, 128, 'morl', 'auto', 'jet', 'bilinear', 'lower', 'Magnitude', 'vertical', 'Continuous Wavelet Transform', 'Time', 'Scale', False
    #wavelet_type = 'morl' # You can choose a different wavelet, e.g., 'cmor', 'morl', 'gaus', etc.
    plots_config = get_plots_config(config)
    wv_config = plots_config['wavelet_transform']
    wv_aspect = wv_config.get('aspect')
    wv_cmap = wv_config.get('cmap')
    wv_interpolation = wv_config.get('interpolation')
    wv_origin = wv_config.get('origin')
    cbar_label = wv_config.get('cbar_label')
    wvcbar_orientation = wv_config.get('cbar_orientation')
    wv_title = wv_config.get('title')
    #wv_xlabel = wv_config.get('xlabel')
    wv_ylabel = wv_config.get('ylabel')
    wv_grid = wv_config.get('grid')
    #scale_range_low, scale_range_max, wavelet_type, wv_aspect, wv_cmap, wv_interpolation, wv_origin, cbar_label, wvcbar_orientation, wv_title, wv_xlabel, wv_ylabel, wv_grid =  1, 128, 'morl', 'auto', 'jet', 'bilinear', 'lower', 'Magnitude', 'vertical', 'Continuous Wavelet Transform', 'Time', 'Scale', False
    return wv_aspect, wv_cmap, wv_interpolation, wv_origin, cbar_label, wvcbar_orientation, wv_title, wv_ylabel, wv_grid

def get_histplot_params(config):
    plots_config = get_plots_config(config)
    histplot_config = plots_config['values_histogram']
    hist_title = histplot_config.get('title')
    hist_xlabel = histplot_config.get('xlabel')
    hist_ylabel = histplot_config.get('ylabel')
    hist_grid_reqd = histplot_config.get('grid')
    hist_yscale = histplot_config.get('yscale')
    bins_set = histplot_config.get('bins')
    density_set = histplot_config.get('density')
    hist_edgecolor = histplot_config.get('edgecolor')
    hist_bgcolor = histplot_config.get('bgcolor')
    hist_lwidth = histplot_config.get('linewidth')
    hist_is_horiz = histplot_config.get('is_horizontal')
    #hist_title, hist_xlabel, hist_ylabel, hist_grid_reqd, hist_yscale, bins_set, density_set, hist_edgecolor, hist_bgcolor, hist_lwidth = 'Histogram of Signal Values', 'Amplitude', 'Frequency', True, 'log', 'auto', True, 'black', 'white', 1
    return hist_title, hist_xlabel, hist_ylabel, hist_grid_reqd, hist_yscale, bins_set, density_set, hist_edgecolor, hist_bgcolor, hist_lwidth, hist_is_horiz

def get_ftplot_params(config):
    ft_config = get_ftplot_config(config)
    ft_bgcolor = ft_config.get('bgcolor')
    ft_title = ft_config.get('title')
    ft_xlabel = ft_config.get('xlabel')
    ft_ylabel = ft_config.get('ylabel')
    ft_yscale = ft_config.get('yscale')
    ft_grid = ft_config.get('grid')
    ft_color = ft_config.get('color')
    ft_linewidth = ft_config.get('linewidth')
    return ft_bgcolor, ft_title, ft_xlabel, ft_ylabel, ft_yscale, ft_grid, ft_color, ft_linewidth

def get_polynt_params(config):
    plots_config = get_plots_config(config)
    polyint_config = plots_config['polyint']
    polynt_color = polyint_config.get('color')
    polynt_lstyle = polyint_config.get('linestyle')
    polynt_lwid = polyint_config.get('linesize')
    coeff_short_format = polyint_config.get('coeff_short_fmt')
    return polynt_color, polynt_lstyle, polynt_lwid, coeff_short_format

def get_plots_tooltip_params(config):
    plots_config = get_plots_config(config)
    legenda_config = plots_config['tooltip']
    lg_enabled = legenda_config.get('enabled')
    lg_fontsz = legenda_config.get('fontsize')
    lg_boxstyle = legenda_config.get('boxstyle')
    lg_vertalign = legenda_config.get('verticalalign')
    lg_bgcolor = legenda_config.get('bgcolor')
    lg_transp = legenda_config.get('transparency')
    lg_xpos = legenda_config.get('xpos_pct')
    lg_ypos = legenda_config.get('ypos_pct')
    return lg_enabled, lg_fontsz, lg_boxstyle, lg_vertalign, lg_bgcolor, lg_transp, lg_xpos, lg_ypos

def get_subplotfiles_params(config):
    out_config = get_output_config(config)
    plotfiles_config = out_config['plot_files']
    subplotfiles_config = plotfiles_config['subplot_files']
    x_expand = subplotfiles_config.get('x_expand')
    y_expand = subplotfiles_config.get('y_expand')
    return x_expand, y_expand

def get_plotfiles_params(config):
    out_config = get_output_config(config)
    plotfiles_config = out_config['plot_files']
    extens = plotfiles_config.get('ext')
    fname_suffix = plotfiles_config.get('filename_suffix')
    tstampfmt_key = 'timestamp_suffix'
    tstamp_suffix_format = plotfiles_config[tstampfmt_key] if (tstampfmt_key in plotfiles_config) else None
    return extens, fname_suffix, tstamp_suffix_format

def get_signal_info_format(config):
    in_data_analysis_config = get_indataanalysis_config(config)
    signalstats_config = in_data_analysis_config['signal_stats']
    out_format = signalstats_config.get('format')
    return out_format

def get_sampfreq_format(config):
    in_data_analysis_config = get_indataanalysis_config(config)
    sampfreq_config = in_data_analysis_config['sampling_frequency']
    out_format = sampfreq_config.get('format')
    return out_format

def get_timewindow_info_format(config):
    in_data_analysis_config = get_indataanalysis_config(config)
    xwindow_config = in_data_analysis_config['x_window']
    out_format = xwindow_config.get('format')
    return out_format

def get_timeslice_info_format(config):
    in_data_analysis_config = get_indataanalysis_config(config)
    xslice_stats_config = in_data_analysis_config['x_slices_stats']
    out_format = xslice_stats_config.get('format')
    return out_format

def get_indataanalysis_config(config):
    processing_config = get_processing_config(config)
    in_data_analysis_config = processing_config['input_data_analysis']
    return in_data_analysis_config

def get_freqplots_config(config):
    plots_config = get_plots_config(config)
    freq_plots_config = plots_config['frequency_plots']
    return freq_plots_config

def get_psdplot_config(config):
    fplots_config = get_freqplots_config(config)
    psd_plot_config = fplots_config['psd']
    return psd_plot_config

def get_ftplot_config(config):
    fplots_config = get_freqplots_config(config)
    ft_plot_config = fplots_config['ft']
    return ft_plot_config

def get_plots_config(config):
    processing_config = get_processing_config(config)
    plots_config = processing_config['plots']
    return plots_config

def get_input_data_config(config):
    input_data_config = config['input_data']
    return input_data_config

def get_processing_config(config):
    proc_config = config['processing_params']
    return proc_config

def get_audio_gen_config(config):
    audio_gen_config = get_audio_config(config)['general']
    return audio_gen_config

def get_audio_config(config):
    audio_config = config['audio']
    return audio_config

def get_output_config(config):
    proc_config = get_processing_config(config)
    out_config = proc_config['output']
    return out_config
