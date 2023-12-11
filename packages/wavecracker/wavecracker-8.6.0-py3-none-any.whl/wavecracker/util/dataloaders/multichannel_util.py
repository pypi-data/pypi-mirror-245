# v. 5.3.0 231111

from common_util import beautified_string, create_rnd_string, is_stdout_debug_on
from config_util import resolve_tabledef_id
from config_tables_util import get_table_hnd, get_table_attributes, get_table_field_ids, get_field_attributes
#, get_table_field_ids, get_field_attributes
import logging

def get_cs_aggregates(channelsets):
    #logger = logging.getLogger(__name__)
    num_samp_list = []
    nc = 0
    mins = 0
    maxs = 0
    if (channelsets):
        nc = sum(len(item['signals']) for item in channelsets)
        for cset in channelsets:
            num_samples = derive_channelset_info(cset)
            num_samp_list.append(num_samples)
        mins = min(num_samp_list)
        maxs = max(num_samp_list)
    return nc, mins, maxs

#print ('qplot: ['Time(s)', 'Channel1', 'Channel2']
def build_table_def_from_cmd(attempt_idx, qplot):
    logger = logging.getLogger(__name__)
    table_def = None
    x_name = qplot[0]
    y_names = qplot[1:]
    y_filetokens = ['y' + str(i) for i in range(1, len(y_names) + 1)]
    table_def = load_inmemory_table(attempt_idx, x_name, 't', y_names, y_filetokens)
    #return 'cmd-' + create_rnd_string(10), table_def
    return table_def['id'], table_def

#csv
def load_table_from_config(attempt_idx, cfg, table_id):
    return load_table_generic(attempt_idx, cfg, table_id, None, None, None, None)


#audio
def load_inmemory_table(attempt_idx, x_field, x_filetoken, yfield_ids, y_filetokens_found):
    all_columns = yfield_ids + [x_field]
    return load_table_generic(attempt_idx, None, None,   all_columns, x_field, x_filetoken, y_filetokens_found)

# audio looks like this:, i.e. passing [Time, L, R]
# {
#    'id': 'in-memory-1',
#    'x_sort': False,
#    'fields': [
#        {'id': 'Time', 'name': 'Time', 'desc': 'Time', 'x_sort': False},
#        {'id': 'L', 'name': 'L', 'desc': 'L', 'x_ref': 'Time', 'x_sort': False},
#        {'id': 'R', 'name': 'R', 'desc': 'R', 'x_ref': 'Time', 'x_sort': False}
#    ]
#}



# !!!!!!!!!!!!!!!!! field_ids is a list of ALL y fields and the x field IN LAST POSITION
# table_id forces csv-like (and field_ids is neglected), otherwise it's non-csv like audio
# with non-csv assumption is: ONE channelset only.
# And except the x_field (aka time), all the others will refer to x_field

def load_table_generic(attempt_idx, cfg, table_id, field_ids, x_field, x_filetoken, y_filetokens):
    logger = logging.getLogger(__name__)
    default_sort = False # applies only in non-csv mode (I cannot reshuffle a binary file like an MP3!)
    #logger.warning('[' + str(attempt_idx) + '] multichannel_util.load_table_generic: check di integrita FORTE - in modalita non-csv ci ')

    is_csv_mode = not (table_id is None)
    mode_desc = 'from configuration file' if is_csv_mode else 'in-memory (embedded)'
    fields_info = '' if is_csv_mode else ' [fields: ' + ', '.join(field_ids) + '; sort option default: ' + str(default_sort) + ']'
    logger.debug('[' + str(attempt_idx) + '] Table definition mode: ' + mode_desc + fields_info)

    table_hnd = get_table_hnd(cfg, table_id) if is_csv_mode else None
    table_df = {}
    table_x_sort = get_table_attributes(table_hnd) if is_csv_mode else default_sort
    table_df = {}
    table_df['id'] = table_id if is_csv_mode else create_rnd_string(10)
    table_df['x_sort'] = table_x_sort
    fields_obj = []

    field_ids_in_scope = get_table_field_ids(table_hnd) if is_csv_mode else field_ids
    logger.debug('[' + str(attempt_idx) + '] \n\n\nIN MEMORY TABLE fields in scope' + str(field_ids_in_scope) + ' \n\n\n')
    field_idx = 0
    for field_id in field_ids_in_scope:
        field_idx = field_idx + 1

        field_ftoken = None
        if is_csv_mode:
            field_name, field_desc, field_xref, field_xsort, field_ftoken = get_field_attributes(table_hnd, field_id)
        else:
            field_name, field_desc, field_xsort = field_id, field_id, default_sort
            #field_xref = x_field if (not field_id in [x_field]) else None
            if (field_id in [x_field]):
                field_xref = None
                field_ftoken = x_filetoken if (not (x_filetoken is None)) else 'x' + str(field_idx)
            else:
                field_xref = x_field
                #x field: >Time<
                #field_ids_in_scope: tutti gli assi; con l'asse X all'ultimo eg: 1/2 (right), 0+1/2 (interleaved), Time
                #lista y_filetokens, tutti i filetokens di asse y, in stesso ordine: 1, I
                # quindi l'espressione che prende quello che mi serve e' y_filetokens[field_ids_in_scope.index(field_id)]
                #logger.debug('[' + str(attempt_idx) + '] #############################################')
                field_ftoken = y_filetokens[field_ids_in_scope.index(field_id)] 
                logger.debug('[' + str(attempt_idx) + '] \n\n debug(' + field_id + ')\n\nx field: > ' + x_field + '<\n\nlista field ids: ' + ', '.join(field_ids) + '<\n\nlista y file tokens: ' + ', '.join(y_filetokens))

        cur_field_def = {}
        cur_field_def['id'] = field_id #'c' + str(field_idx) #
        cur_field_def['name'] = field_name
        cur_field_def['desc'] = field_desc
        cur_field_def['filetoken'] = field_ftoken if (not (field_ftoken is None)) else ('f' + str(field_idx))

        if (not (field_xref is None)):
            cur_field_def['x_ref'] = field_xref
        if (not (field_xsort is None)):
            cur_field_def['x_sort'] = field_xsort
        fields_obj.append(cur_field_def)
    table_df['fields'] = fields_obj
    #logger.debug('[' + str(attempt_idx) + '] Table definition internal in-memory representation: ' + beautified_string(table_df))
    debug_tabledef(attempt_idx, table_df, 'after creation', 'mode: ' + mode_desc + fields_info)
    return table_df

def debug_tabledef(attempt_idx, obj, contextstr, mode_infostr):
    logger = logging.getLogger(__name__)
    td_show = is_stdout_debug_on()
    context = '' if (contextstr is None) else ' (' + contextstr + ')'
    mode_info = '' if (mode_infostr is None) else '{' + mode_infostr + '}'
    td_2display = '\n\n\n [' + str(attempt_idx) + '] \n TABLE DEFINITION' + context + ': ' + beautified_string(obj) + '\n\n' + mode_info + ' \n\n\n'
    logger.info(td_2display) if (td_show) else logger.debug(td_2display)


def build_table_def(attempt_idx, root_config, table_config, load_config, table_def_override):
    logger = logging.getLogger(__name__)
    table_def_id = resolve_tabledef_id(root_config, load_config, table_def_override)
    #print('xxxxxxxxxxxxxxxxxxxxxxxx id: ' + table_def_id)
    #import sys
    #sXys.exit(1)
    table_df = load_table_from_config(attempt_idx, table_config, table_def_id)
    return table_def_id, table_df

def build_cs_x_axis_obj(idx, x_axis_id, x_name, x_ax_desc, x_ax_filetoken):
    xobj_ft = x_ax_filetoken if (not (x_ax_filetoken is None)) else 'x' + str(idx) #x_axis_id
    cs_xaxis_object = {
                'id': x_axis_id,
                'filename_token': xobj_ft,
                'field': x_name,
                'desc': x_ax_desc
            }
    return cs_xaxis_object

def build_cs_y_axis_obj(idx, y_axis_id, y_ax_field, x_sort_on, x_data_pointer, y_data_pointer, y_ax_name, y_filetoken):
    yobj_ft = 'y' + str(idx) if ((y_filetoken is None) or (y_filetoken in ['NA'])) else y_filetoken
    cs_yaxis_object = {
                'id': y_axis_id,
                'filename_token': yobj_ft,
                'field': y_ax_field,
                'x_sorted': x_sort_on,
                'x_data': x_data_pointer,
                'y_data': y_data_pointer,
                'desc': y_ax_name
            }
    return cs_yaxis_object

def build_single_channelset(x_axis_obj, signals_obj):
    single_cs_obj = {
                'x_axis': x_axis_obj,
                'signals': signals_obj
            }
    return single_cs_obj

# build channelsets: raw_data is the 'data' object out of the csv
# is_psortable has to be True for all arrays that can be sorted with the pandas .sort_values callable
#     (so at the current 4.1.0 stage it is YES for the csv loaded, NO for the audio loaders)
# x_vals: array of times. When specified, it will apply to all axes definitions.
#     (so at the current 4.1.0 stage, with use it for the audio loaders, and the csv loaders will send None)
# note also that, if you specify a x_vals, then the is_psortable does not even apply
# in teoria potrei implementare il caso in cui PASSO i tempi, ma scelgo ANCHE il sort.
# solo che e' complicato perche' ho DUE array distinti con cui giocare, quello dei tempi e quello delle y.
# fattibile, ma non per ora
#
# y_filetokens_found: suggerimento per i filetoken delle colonne'y'.
# se assente, la build_channelsets li cerca in table_def. Se neanche li' li trova, allora sono 'y1', 'y2', ...
def build_channelsets(attempt_idx, table_def, x_columns_found, y_columns_found, y_filetokens_found, raw_data, is_psort_ok, x_vals):
    logger = logging.getLogger(__name__)
    #beautified_string
    min_num_samples, max_num_samples = 0, 0
    channelsets_list = []
    num_samples = 0
    num_samples_list = []
    samples_count_ok = False
    min_ns_val, max_ns_val = 0, 0
    x_count = 0
    time_vals_spec = (not (x_vals is None))
    is_psortable = is_psort_ok and (not time_vals_spec)
    logger.debug('[' + str(attempt_idx) + '] build_channelsets - begin; x_vals specified: ' + str(time_vals_spec))
    logger.debug('[' + str(attempt_idx) + '] build_channelsets - begin; is_panda-sortable: ' + str(is_psortable))

    #filename_token_is_id = True
    #table_filetoken = table_def['id'] if filename_token_is_id else 't'
    table_x_sort_on = table_def['x_sort'] if ('x_sort' in table_def) else False
    for curr_x_name in x_columns_found:
        x_count = x_count + 1
        logger.debug('[' + str(attempt_idx) + '] CS-debug: new x-axis (' + str(x_count) + '): ' + curr_x_name)
        curr_x_object = [f for f in table_def['fields'] if ('x_ref' not in f) and (f['name'] == curr_x_name)][0]
        curr_x_axis_id = curr_x_object['id']
        x_ax_desc = curr_x_object['desc'] if ('desc' in curr_x_object) else curr_x_name
        x_ax_filetoken = curr_x_object['filetoken'] if ('filetoken' in curr_x_object) else 'x' + str(y_count)
        y_count = 0
        curr_columns_list = []
        logger.debug('\n\n[' + str(attempt_idx) + ']   **************************** PRE *************************** \n\n')
        logger.debug('\n\n[' + str(attempt_idx) + '] curr_x_axis_id: ' + curr_x_axis_id)
        logger.debug('\n\n[' + str(attempt_idx) + '] y_columns_found: ' + str(y_columns_found))
        logger.debug('\n\n[' + str(attempt_idx) + '] table_def: ' + str(table_def))
        y_objects = [f for f in table_def['fields'] if ((f['name'] in y_columns_found) and ('x_ref' in f) and (f['x_ref'] == curr_x_axis_id))]
        logger.debug('\n\n[' + str(attempt_idx) + ']   **************************** POST *************************** \n\n')
        #for curr_y_object in [f for f in table_def['fields'] if ((f['name'] in y_columns_found) and ('x_ref' in f) and (f['x_ref'] == curr_x_axis_id))]:
        #if (time_vals_spec):
        #    y_objects = 
        for curr_y_object in y_objects:

            y_count = y_count + 1
            logger.debug('[' + str(attempt_idx) + '] CS-debug: new signal (' + str(x_count) + ', ' + str(y_count) + '): ' + curr_x_name)
            curr_y_axis_id = curr_y_object['id'] if ('id' in curr_y_object) else 'y' + str(y_count)
            y_ax_field = curr_y_object['name']
            y_ax_name = curr_y_object['desc'] if ('desc' in curr_y_object) else y_ax_field
            y_ax_filetoken = curr_y_object['filetoken'] if ('filetoken' in curr_y_object) else 'y' + str(y_count)
            x_sort_on = (curr_y_object['x_sort']) if ('x_sort' in curr_y_object) else table_x_sort_on
            logger.debug('[' + str(attempt_idx) + '] CS-debug: Signal info (id): ' + curr_y_axis_id)

            #si potrebbe isolare questa che vale solo per il csv
            x_data_pointer = x_vals if (time_vals_spec) else raw_data[curr_x_name]
            y_data_pointer = raw_data[y_ax_field]
            no_data = ((x_data_pointer is None) or (y_data_pointer is None) or (len (x_data_pointer) == 0) or (len (y_data_pointer) == 0))
            if (no_data):
                logger.error('[' + str(attempt_idx) + '] Critical internal error: NO DATA while building the channels set (detail: CS[' + curr_x_name + ', ' + y_ax_field + '])')
            else:
                if (x_sort_on and is_psortable):
                    logger.info('[' + str(attempt_idx) + '] [x=' + curr_x_name + ', y=' + y_ax_field + '] Sorting by: ' + curr_x_name)

                    #slices and copies
                    reduced_data = raw_data[[curr_x_name, y_ax_field]]
                    #pandas call
                    reduced_data.sort_values(by=curr_x_name, inplace=True)
                    x_data_pointer = reduced_data[curr_x_name]
                    y_data_pointer = reduced_data[y_ax_field]

                #y_filetoken = eval_y_filetoken(table_def, y_filetokens_found, y_count)
                update_nslist(attempt_idx, num_samples_list, x_count, y_count, curr_x_name, y_ax_field, x_data_pointer, y_data_pointer)
                curr_y_axis = build_cs_y_axis_obj(y_count, curr_y_axis_id, y_ax_field, x_sort_on, x_data_pointer, y_data_pointer, y_ax_name, y_ax_filetoken)
                curr_columns_list.append(curr_y_axis)

        chn_set = build_single_channelset(build_cs_x_axis_obj(x_count, curr_x_axis_id, curr_x_name, x_ax_desc, x_ax_filetoken), curr_columns_list)
        channelsets_list.append(chn_set)

    # cannot use beautify_string for this, as there are the two HUGE fields x_data and y_data
    debug_channelsets(attempt_idx, channelsets_list, 'after built')
    if (len(num_samples_list) > 0):
        min_num_samples = min(num_samples_list, key=lambda x: x['num_sampl'])['num_sampl']
        max_num_samples = max(num_samples_list, key=lambda x: x['num_sampl'])['num_sampl']
    else:
        logger.error('[' + str(attempt_idx) + ']: Critical internal error, list of num_samples totals is EMPTY')

    samples_count_ok = (min_num_samples == max_num_samples)
    return min_num_samples, max_num_samples, samples_count_ok, channelsets_list
 

def update_nslist(attempt_idx, nslist, x_count, y_count, x_fname, y_fname, x_data, y_data):
    logger = logging.getLogger(__name__)
    fname_suff = '-' + str(x_count) + '-' + str(y_count)
    nsx, nsy = len(x_data), len(y_data)
    nslist.append({'field': x_fname + fname_suff, 'num_sampl': nsx})
    nslist.append({'field': y_fname + fname_suff, 'num_sampl': nsy})
    logger.debug('[' + str(attempt_idx) + ']: Updated num samples list (items: ' + str(len(nslist)) + '), new element: [' + x_fname + ': ' + str(nsx) + ', ' + y_fname + ': ' + str(nsy) + ']')

# cannot use beautify_string for this, as there are the two HUGE fields x_data and y_data
def debug_channelsets(attempt_idx, obj, contextstr):
    attempts_str = '[' + str(attempt_idx) + '] ' if (not (attempt_idx is None)) else ''
    logger = logging.getLogger(__name__)
    cs_show = is_stdout_debug_on()
    context = '' if (contextstr is None) else ' (' + contextstr + ')'
    cs_2display = '\n\n\n [' + str(attempt_idx) + '] \n CHANNELSETS' + context + ': ' + channelsets_as_string(obj) + ' \n\n\n'
    logger.info(cs_2display) if (cs_show) else logger.debug(cs_2display)

def get_channelset_x_axis(channelset):
    return channelset['x_axis']

def get_channelset_signals(channelset):
    return channelset['signals']

def get_signal_xy_data(signal):
    return signal['x_data'], signal['y_data']

def set_signal_xy_data(signal, x_values, y_values):
    signal['x_data'], signal['y_data'] = x_values, y_values

def derive_channelset_info(channelset):
    num_samples = len(get_channelset_signals(channelset)[0]['x_data'])
    return num_samples

def set_numsamples_predownsampling(channelset, num_samples_pre):
    logger = logging.getLogger(__name__)
    x_axis = get_channelset_x_axis(channelset) # channelset['x_ax-is']
    logger.debug('x axis - assigning num samples pre: ' + str(num_samples_pre))
    x_axis['size_pre_downsmpl'] = num_samples_pre

def get_channelset_attributes(channelset):
    x_axis = get_channelset_x_axis(channelset) #channelset['x_ax-is']
    x_field = x_axis['field']
    num_samples_pre = x_axis['size_pre_downsmpl'] if 'size_pre_downsmpl' in x_axis else None
    return x_field, x_axis['desc'] if ('desc' in x_axis) else x_field, x_axis['avg_x_diff'], x_axis['filename_token'], num_samples_pre

def set_x_axis_calc_attributes(channelset, avg_time_difference):
    logger = logging.getLogger(__name__)
    x_axis = get_channelset_x_axis(channelset) #channelset['x_a-xis']
    logger.debug('x axis - assigning average_x_difference: ' + str(avg_time_difference))
    x_axis['avg_x_diff'] = avg_time_difference

def set_signal_calc_attributes(signal, sign_avg):
    logger = logging.getLogger(__name__)
    logger.debug('Signal - assigning signal avg: ' + str(sign_avg))
    signal['y_avg'] = sign_avg

def channelsets_as_string(cssobj):
    strng = '\n\n ['
    cscount = 0
    for cur_cset in cssobj:
        cscount = cscount + 1
        if (cscount > 1):
            strng = strng + ',\n'
        strng = strng + '\n  channelset #' + str(cscount) +  ': ' + channelset_as_str(cur_cset)
    strng = strng + '\n  ]'
    return strng

def get_signal_attributes(signal):
    s_field = signal['field']
    return s_field, signal['desc'] if ('desc' in signal) else s_field, signal['filename_token']

def get_signal_data(signal):
    return signal['x_data'], signal['y_data'], signal['y_avg']

def channelset_as_str(csobj):
    strng = '{'
    if ('x_axis' in csobj):
        strng = strng + '\n    x_axis: {'
        x_axisObj = get_channelset_x_axis(csobj) # csobj['x_axxis']
        strng = strng + '\n      id:             ' + x_axisObj['id']
        strng = strng + '\n      filename_token: ' + x_axisObj['filename_token']
        strng = strng + '\n      field:          ' + x_axisObj['field']
        strng = strng + '\n      desc:           ' + x_axisObj['desc']
        if ('avg_x_diff' in x_axisObj):
            strng = strng + '\n      avg_x_diff:     ' + str(x_axisObj['avg_x_diff'])
        if ('size_pre_downsmpl' in x_axisObj):
            strng = strng + '\n      size_pre_downsmpl:     ' + str(x_axisObj['size_pre_downsmpl'])
        #print_dict_fields(x_axisObj, ['id', 'filename_token', 'field', 'desc'])
        scount = 0
        for cur_signal in csobj['signals']:
            scount = scount + 1
            strng = strng + '\n        Signal #' + str(scount)
            strng = strng + '\n          id:             ' + cur_signal['id']
            strng = strng + '\n          filename_token: ' + cur_signal['filename_token']
            strng = strng + '\n          field:          ' + cur_signal['field']
            if ('x_sorted' in cur_signal):
                strng = strng + '\n          x_sorted:       ' + str(cur_signal['x_sorted'])
            x_data_pointer_len = len(cur_signal['x_data'])
            strng = strng + '\n          x_data:         ' + '<array (' + str(x_data_pointer_len) + ')>'
            y_data_pointer_len = len(cur_signal['y_data'])
            strng = strng + '\n          y_data:         ' + '<array (' + str(y_data_pointer_len) + ')>'
            if ('y_avg' in cur_signal):
                strng = strng + '\n          y_avg:          ' + str(cur_signal['y_avg'])
            strng = strng + '\n          desc:           ' + cur_signal['desc']

    strng = strng + '\n    }'
    return strng

# this is how the internal tabledef looks:
#table_df_OLD= {
#    'id': 'td1',
#    'x_sort': True,
#    'fields': [
#        {
#            'id': 'time1',
#            #'filename_fragment': 't' - if absent, then f1, f2, ..id or a progressive, depending on some different conf
#            'name': 'Time(s)',
#            'desc': 'Time'
#        },
#        {
#            'id': 'time2',
#            'name': 'Time2(s)',
#            'desc': 'Time'
#        },
#        {
#            'id': 'field3',
#            'name': 'Channel1',
#            'desc': 'Original Signal 1 sorted',
#            'x_ref': 'time1',
#            'x_sort': True # sort only if specified and if true, applies only if x_ref is presente - best to do is NOT in place
#        },
#        {
#            'id': 'field3a',
#            'name': 'Channel1',
#            'desc': 'Original Signal 1 unsorted',
#            'x_ref': 'time1'
#        },
#        {
#            'id': 'field4',
#            'name': 'Channel2',
#            'desc': 'Original Signal 2',
#            'x_ref': 'time2'
#        },
#        {
#            'id': 'field5',
#            'name': 'Channel2',
#            'desc': 'Original Signal 2',
#            'x_ref': 'time2'
#        }
#    ]
#}


# this is how the generated channelset map looks like
#[
#    {
#        'x_axis': {
#            'id': 'field1',
#            'filename_token': 'field1',
#            'field': 'Time(s)',
#            'desc': 'Time'
#             avg_x_diff: 0.33232,
#             size_pre_downsmpl =
#        },
#        'signals': [
#            {
#                'id': 'field3',
#                'filename_token': 'field3',
#                'field': 'Channel1',
#                'x_sorted': True,
#                'x_data': <data pointer>,
#                'y_data':  <data pointer>,
#                'desc': 'Original Signal 1'
#            },
#            {
#                'id': 'field5',
#                'filename_token': 'field5',
#                'field': 'Channel2',
#                'x_sorted': False,
#                'x_data': <data pointer>,
#                'y_data':  <data pointer>,
#                y_avg:          0.26313661332917637
#                'desc': 'Original Signal 2'
#            }
#        ]
#     },
#     .......next x-axis + signals group ....
#]


