# v. 5.6.0 231114

import logging
import re

# retrieves a guess for decimal and thousand separator, out of a supposed string made of candidates
# The input is a float MINUS all the digits, minus also +, -, E, e
# typical input is: ,,,.. if there are two distinct, the 1st is supposed to be the thousands sep, the second is decimal
def get_separ_from_string(s):
    decimal_sep, thous_sep = None, None
    maxsz = 2
    seen_chars = []
    num_seen = 0
    for char in s:
        if (not (char in seen_chars)):
            seen_chars.append(char)
            num_seen = num_seen + 1
            if (maxsz == num_seen):
                break
    if (num_seen > 0):
        if (num_seen < 2):
            decimal_sep = seen_chars[0]
        else:
            thous_sep = seen_chars[0]
            decimal_sep = seen_chars[1]

    #print(' <<<<<<<<<<<<<<<<<<<<<<<<<  ' + s + ' ' + str(decimal_sep) + ' ' + str(thous_sep))
    return decimal_sep, thous_sep

# retrieves a guess for decimal and thousand separator, out of a supposed float string
def exclude_from_string(str, excl_pattern):
    # Strip and trim the string
    trimmed_str = str.strip()
    # Remove all characters except punctuation (decimal point and thousands separator)

    #cleaned_str = re.sub(r'[\d\+\-eE_]', '', trimmed_str)
    cleaned_str = excl_pattern.sub('', trimmed_str)

    decimal_sep, thous_sep = get_separ_from_string(cleaned_str)
    return decimal_sep, thous_sep

# retrieves a guess for decimal and thousand separator, out of a supposed CSV file, starting the search from skip_rows+1
def detect_float_separators(attempt_idx, file_path, c_encoding, field_sep, comment_pfix, skip_rows):
    logger = logging.getLogger(__name__)
    decimal_sep, thous_sep = None, None
    detection_ok = False
    dec_seps_found = []
    thous_seps_found = []
    try:
        excl_pattern_str = '[\d\+\-eE_]'
        logger.debug('[' + str(attempt_idx) + '] float string exclusion pattern: ' + excl_pattern_str)
        excl_pattern = re.compile(excl_pattern_str)

        with open(file_path, 'r', encoding=c_encoding) as in_file:
            #for num, data_line_d in enumerate(in_file, 1):
            for num, data_line_d in enumerate(in_file, start=1):
                if (num > skip_rows):
                    data_line = data_line_d.strip() #fondamentale togliere l'a capo finale!!! salta tutto diversamente!!
                    #print('xxxxxxxxxxxxxxxxxxxxxxxx ' + data_line)
                    line_to_be_processed = (not (data_line.startswith(comment_pfix))) if comment_pfix else (True)
                    if (line_to_be_processed):
                        field_values = data_line.split(field_sep)
                        for value in field_values:
                            cur_dec_sep, cur_thous_sep = exclude_from_string(value, excl_pattern)
                            #print('LINE ['+str(num)+'] ' + str((cur_dec_sep, cur_thous_sep)))
                            if cur_dec_sep and (not (cur_dec_sep in dec_seps_found)):
                                dec_seps_found.append(cur_dec_sep)
                            if cur_thous_sep and (not (cur_thous_sep in thous_seps_found)):
                                thous_seps_found.append(cur_thous_sep)
                        if (len(dec_seps_found) != 1) or (len(thous_seps_found) > 1):
                            break
        num_thous_found = len(thous_seps_found)
        detection_ok = (len(dec_seps_found) == 1) and (num_thous_found < 2)
        if (detection_ok):
            decimal_sep, thous_sep = dec_seps_found[0], thous_seps_found[0] if (num_thous_found > 0) else None
            logger.info('[' + str(attempt_idx) + '] Numeric separators detection complete.')
            logger.debug('[' + str(attempt_idx) + '] detect_float_separators, values before end: decimal sep.: ' +  str(decimal_sep)+ ', thousands sep.: ' + str(thous_sep))
        else:
            logger.warning('[' + str(attempt_idx) + '] Separator detection did not succeed.')
            logger.warning('[' + str(attempt_idx) + '] Decimal separators found:   ' + str(dec_seps_found))
            logger.warning('[' + str(attempt_idx) + '] Thousands separators found: ' + str(thous_seps_found))
    except Exception as e:
        detection_ok, decimal_sep, thous_sep = False, None, None
        logger.warning('[' + str(attempt_idx) + '] Separator detection FAILED (' + str(e) + ')')
    return detection_ok, decimal_sep, thous_sep
