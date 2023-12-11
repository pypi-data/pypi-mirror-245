# v. 5.2.0 231111

import logging

def get_table_field_ids(table_hnd):
    return table_hnd['fields']

def get_field_attributes(table_hnd, field_id):
    field_hnd = table_hnd['fields'][field_id]
    field_name = field_hnd['name']
    field_desc = field_hnd['desc'] if ('desc' in field_hnd) else field_name
    xref_key = 'x_ref'
    xsort_key = 'x_sort'
    ftoken_key = 'filename_token'

    field_ftoken = None
    if (not (field_hnd is None)) and ftoken_key in field_hnd:
        field_ftoken = field_hnd[ftoken_key]

    field_xref = None
    if (not (field_hnd is None)) and xref_key in field_hnd:
        field_xref = field_hnd[xref_key]

    field_xsort = None
    if (not (field_hnd is None)) and xsort_key in field_hnd:
        field_xsort = field_hnd[xsort_key]
    return field_name, field_desc, field_xref, field_xsort, field_ftoken

def get_table_attributes(tabl_hnd):
    xsort_key = 'x_sort'
    t_xsort = False if (tabl_hnd is None) or (not (xsort_key in tabl_hnd)) else tabl_hnd.get[xsort_key]
    return t_xsort

def get_table_hnd(tconfig, table_id):
    input_data = get_input_data_config(tconfig)
    try:
        tabl_hnd = input_data['table_defs'][table_id]
    except Exception as e:
        raise Exception('Table not found: ' + table_id + ' (check command line arguments and tables configuration file)')        
    return tabl_hnd

def get_input_data_config(tconfig):
    inputd_key = 'input_data'
    input_data_tconfig = tconfig[inputd_key] if (tconfig and (inputd_key in tconfig)) else None
    return input_data_tconfig

