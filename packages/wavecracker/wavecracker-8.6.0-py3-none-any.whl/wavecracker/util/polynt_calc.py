# v. 8.5.0 231123

import numpy as np
import logging

#input: the command line arg made of a sequence of int:float,float
#output: collection of:
#        (hi, low, degree, coeffs, sliced_time, sliced_signal, interpolated_signal)
def eval_polynt_data(cs_index, channel_count, pol_int_req, x_vals, y_vals):
    logger = logging.getLogger(__name__)
    logger.info('Calculating interpolations ...')
    log_head = '['+str(cs_index)+']['+str(channel_count)+'] '
    polint_data = []
    x_sz = 0 if (x_vals is None) else len(x_vals)
    y_sz = 0 if (y_vals is None) else len(y_vals)
    if ((x_sz > 0) and (x_sz == y_sz)):
        min_x = np.min(x_vals)
        max_x = np.max(x_vals)
        nsamples = x_sz
        for curr_interp_req in pol_int_req:
            logger.debug(log_head + 'Begin interpolation definition processing: ' + curr_interp_req)
            try:
                first_aggreg = curr_interp_req.strip().split(':')
                pol_degree = int(first_aggreg[0])
                interp_interval_elements = (first_aggreg[1]).split(',')
                interp_lo, interp_hi = float(interp_interval_elements[0]), float(interp_interval_elements[1])
                if (interp_lo < interp_hi):
                    #mask = (x_vals >= interp_lo) & (x_vals <= interp_hi)
                    # Get indices where the condition is true
                    indices = np.where((x_vals >= interp_lo) & (x_vals <= interp_hi))[0]
                    sliced_x = x_vals[indices]
                    nsliced_samples = len(sliced_x)
                    if (nsliced_samples > 0):
                        sliced_y = y_vals[indices]
                        coeffs = np.polyfit(sliced_x, sliced_y, deg=pol_degree)
                        sliced_x_min, sliced_x_max = np.min(sliced_x), np.max(sliced_x)
                        logger.info(log_head + 'Polyfit (deg.: ' + str(pol_degree) + ', range: [' + str(sliced_x_min) + '-' + str(sliced_x_max) + '], subset sz.: ' + str(nsliced_samples) + ') coeffs: ' + ', '.join(str(c) for c in coeffs))
                        ffit = np.poly1d(coeffs)
                        interpolated_signal = ffit(sliced_x)
                        #logger.info('\n\n range calc: '+str(sliced_x_min)+'-'+str(sliced_x_max)+' \n\n')
                        polint_data.append((nsliced_samples, pol_degree, sliced_x_min, sliced_x_max, coeffs, sliced_x, sliced_y, interpolated_signal))
                    else:
                        logger.warn(log_head + 'Invalid interpolation definition ' + curr_interp_req + ': no data')
                else:
                    logger.warn(log_head + 'Invalid interpolation definition ' + curr_interp_req + ': LO should be lower than HI')
            except Exception as e:
                logger.exception(log_head + 'Interpolation definition ' + curr_interp_req + ' had errors: ' + str(e))
    else:
        logger.warning(log_head + 'No interpolations to evaluate: axis do NOT have same size or do not contain data (x: ' + str(x_sz) + ', y: ' + str(y_sz) + ')')
    return polint_data
