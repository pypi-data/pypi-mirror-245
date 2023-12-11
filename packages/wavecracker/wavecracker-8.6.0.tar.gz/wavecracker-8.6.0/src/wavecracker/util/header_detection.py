# v. 6.1.0 231115

import logging
import re

def guess_csv_header(attempt_idx, file_path, c_encoding, sep_list, x_fields, y_fields):
    logger = logging.getLogger(__name__)
    #separator_guess, line_guess = None, None
    guesses = []
    best_score = 0
    logger.debug('[' + str(attempt_idx) + '] Header detection - begin - separators: ' + str(sep_list))
    with open(file_path, 'r', encoding=c_encoding) as file:
        for line_num, line in enumerate(file, 1):
            # Split the line using various potential separators
            for separator in sep_list:
                #line_fields = line.strip().split(separator)
                line_fields = re.split(f'{separator}\s*', line.strip())

                #  #pattern = re.compile(re.escape(separator), re.IGNORECASE)
                #  #line_fields = pattern.split(line.strip())
                #  #pattern = re.compile(f'({separator}|\S+)') #, re.IGNORECASE)
                #  #line_fields = pattern.findall(line)

                # Check if at least one x field is present
                xfields_found = [xfield in line_fields for xfield in x_fields]
                num_xfields = sum(xfields_found)
                num_yfields = 0
                if (num_xfields > 0):
                    yfields_found = [yfield in line_fields for yfield in y_fields]
                    num_yfields = sum(yfields_found)
                    # Calculate the score based on the presence of y fields
                    score = num_xfields + num_yfields

                    # Update the best guess if the current line has a higher score
                    if (score >= best_score):
                        #separator_guess, line_guess = separator, line_num
                        guesses.append((separator, line_num))
                        best_score = score
                        logger.debug('[' + str(attempt_idx) + '] Header guess (' + str(best_score) + '): ' + str(line_num) + ', sep: >' + separator + '<')

    #return line_guess, separator_guess
    return guesses
