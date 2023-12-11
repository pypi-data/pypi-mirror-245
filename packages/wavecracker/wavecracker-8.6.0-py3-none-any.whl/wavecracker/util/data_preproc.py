# v. 1.4.0 231029

import numpy as np
import logging

class DataPreprocessor:
    def __init__(self, sig_values, signal_avg_val, remove_dc_offs):
        self.signal_values = sig_values
        self.signal_avg_value = signal_avg_val
        self.remove_dc_offset = remove_dc_offs

    def preprocess(self):
        logger = logging.getLogger(__name__)
        logger.debug('Preprocessing: begin')

        logger.debug('DC offset removal requested: ' + str(self.remove_dc_offset))
        if (self.remove_dc_offset):
            sig_values_new = self.signal_values - self.signal_avg_value
            logger.info('DC offset removed')
        else:
            sig_values_new = self.signal_values
        logger.debug('Preprocessing: end')
        return sig_values_new
