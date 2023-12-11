# v. 8.6.0 231211

import numpy as np
from scipy.signal import find_peaks, welch, hilbert
#import pywt

from config_util import get_psdcalc_params, get_sampfreq_format, get_wvletcalc_params
import logging

class SignalTransformer:
    def __init__(self, config_hnd, num_of_samples, average_time_difference, signal_values, sign_envel_reqd, ft_phase_reqd, psd_reqd, frequency_filter, wavelet_reqd, inst_freq_reqd):
        self.num_samples = num_of_samples
        self.avg_time_slice = average_time_difference
        self.signal = signal_values
        self.cfg_hnd = config_hnd
        self.sign_envel_required = sign_envel_reqd
        self.ft_phase_required = ft_phase_reqd
        self.psd_required = psd_reqd
        self.freq_filter = frequency_filter
        self.wavelet_required = wavelet_reqd
        self.instant_freq_reqd = inst_freq_reqd
        #self.poly_int_req = poly_int

    def transform(self):
        logger = logging.getLogger(__name__)
        num_freq_vals = 0
        #poly_int_data = []
        ft_phase = None
        sig_filtered = None
        signal_peaks = None
        psd_x_axis_vals, psd_y_axis_vals = None, None
        wv_scales, wavelet_transform_data, wavelet_type = None, None, None
        instant_freq = None
        # Calculate Fourier transform
        sampl_freq = 1 / self.avg_time_slice  # Sampling frequency
        fmt_sf = get_sampfreq_format(self.cfg_hnd) #'.20E'
        logger.info('Sampling frequency: ' + format(sampl_freq, fmt_sf))
        frequencies = sampl_freq * np.fft.fftshift(np.fft.fftfreq(self.num_samples))  # Frequency axis
        num_freq_vals = len(frequencies)

        fmt_freqval = '.20E' # get_freq_info_format(self.cfg_hnd) #'.20E'
        freq_min = np.min(frequencies)
        freq_max = np.max(frequencies)
        logger.info('Frequency points: ' + str(num_freq_vals))
        logger.info('Frequency axis range: ' + format(freq_min, fmt_freqval) + '/' + format(freq_max, fmt_freqval))
        logger.info('Calculating Fourier transform ...')
        signal_fft = np.fft.fftshift(np.fft.fft(self.signal, self.num_samples))
        logger.debug('Fourier transform calculated')
        if (self.psd_required):
            logger.info('Calculating PSD ...')
            scaling_set, is_onesided = get_psdcalc_params(self.cfg_hnd)
            freqs_psd, psd = welch(self.signal, fs=sampl_freq, nperseg=len(self.signal), scaling=scaling_set, return_onesided=is_onesided)
            psd_x_axis_vals = (freqs_psd if is_onesided else frequencies)
            psd_y_axis_vals = np.fft.fftshift(psd)
            logger.debug('PSD calculated')
        if (self.sign_envel_required):
            logger.info('Calculating Peaks ...')
            signal_peaks, _ = find_peaks(self.signal)
            logger.debug('Peaks calculated')
        if (self.ft_phase_required):
            logger.info('Calculating Phase ...')
            ft_phase = np.angle(signal_fft)
            logger.debug('Phase calculated')
        if (self.wavelet_required):
            try:
                import pywt
            except ImportError as ie:
                logger.error('Module \'pywt\' cannot be loaded (error message was: ' + str(ie) + '). Impact: Wavelet Transform plots are DISABLED')
            else:
                scale_range_low, scale_range_max, wavelet_type = get_wvletcalc_params(self.cfg_hnd)
                logger.info('Calculating Wavelet Transformation (type: ' + wavelet_type + ') ...')
                wv_scales = np.arange(scale_range_low, scale_range_max)  # Adjust the range of scales as needed
                wv_coeffs, _ = pywt.cwt(self.signal, wv_scales, wavelet_type)
                wavelet_transform_data = np.abs(wv_coeffs)
                logger.debug('Wavelet Transformation calculated')
        if (self.instant_freq_reqd ):
            logger.info('Calculating istantaneous frequency ...')
            # Calculate the analytic signal using the Hilbert transform self.time, self.signal
            analytic_signal = hilbert(self.signal)
            # Calculate the instantaneous phase and frequency
            instant_phase = np.unwrap(np.angle(analytic_signal))
            instant_freq = np.diff(instant_phase) / (2 * np.pi) * sampl_freq  # Multiply by the sampling rate
            logger.debug('Istantaneous frequency calculated')

        if (not (self.freq_filter is None)):
            logger.info('Calculating Filtered Signal (mask: ' + str(self.freq_filter) + ')...')
            #sig_filtered = self.signal + 0.1
            sig_filtered = np.real(filter_frequencies_excl(frequencies, signal_fft, self.freq_filter))
            logger.debug('Filtered Signal calculated')
        # returning raw sig_filtered caused a WARNING
        # returning np.abs representation in the plot is not correct
        # with REAL, all fine
        #if ((not (self.poly_int_req is None)) and (len(self.poly_int_req) > 0))
        #    poly_int_data = eval_polynt_data(self.poly_int_req, self.signal)
        return num_freq_vals, sampl_freq, frequencies, signal_fft, np.abs(signal_fft), ft_phase, sig_filtered, signal_peaks, psd_x_axis_vals, psd_y_axis_vals, wv_scales, wavelet_transform_data, wavelet_type, instant_freq

def filter_frequencies_excl(frequencies, signal_fft, freqs_mask):
    logger = logging.getLogger(__name__)
    filtered_signal = None
    filtered_signal_fft = signal_fft.copy()
    #for cur_range in freqs_mask.split('|'):
    for cur_range in freqs_mask:
        filtered_signal_fft = filter_frequencies_range_excl(frequencies, filtered_signal_fft, cur_range)
    # Perform the inverse Fourier transform to obtain the filtered signal
    filtered_signal = np.fft.ifft(np.fft.ifftshift(filtered_signal_fft))
    return filtered_signal

def filter_frequencies_range_excl(freqs, sign_fft, freqs_range):
    logger = logging.getLogger(__name__)
    range_tokens = freqs_range.split(',')
    range_len = len(range_tokens)
    logger.debug('  Filtering for range: ' + freqs_range + ' (tokens: ' + str(range_len) + ')')
    try:
        if (len(freqs_range) > 1):
            freq_low = (range_tokens[0]).strip()
            freq_high = (range_tokens[1]).strip()
            low_is_minus_infinite = (freq_low == '')
            high_is_infinite = (freq_high == '')
            both_infinite = low_is_minus_infinite and high_is_infinite
            logger.debug('    low:  ' + str(freq_low) + ' (-infinite: ' + str(low_is_minus_infinite) + ')')
            logger.debug('    high: ' + str(freq_high) + ' (+infinite: ' + str(high_is_infinite) + ')')
            # Define the frequency range
            # Create a frequency mask to exclude the specified range
            if (not both_infinite):
                if (low_is_minus_infinite):
                    logger.debug('    Range is open to the LEFT')
                    freq_mask = (np.abs(freqs) < float(freq_high))
                else:
                    if (high_is_infinite):
                        logger.debug('    Range is open to the RIGHT')
                        freq_mask = (np.abs(freqs) > float(freq_low))
                    else:
                        logger.debug('    Range is CLOSED')
                        freq_mask = (np.abs(freqs) > float(freq_low)) & (np.abs(freqs) < float(freq_high))
                # Apply the mask to the Fourier transform
                sign_fft[freq_mask] = 0  # Set the frequencies inside the range to zero
    except Exception as e:
        logger.warning('Filtering range ' + freqs_range + ' resulted in errors (' + str(e) + ') and will be skipped')
        #logger.exception('Filtering range ' + freqs_range + ' resulted in errors (' + str(e) + ') and will be skipped')
    return sign_fft

#def filter_frequencies_incl(frequencies, signal_fft, freqs_mask):
#    logger = logging.getLogger(__name__)
#    filtered_signal = None
#    filtered_signal_fft = signal_fft.copy()
#    #for cur_range in freqs_mask.split('|'):
#    for cur_range in freqs_mask:
#        filtered_signal_fft = filter_frequencies_range_incl(frequencies, filtered_signal_fft, cur_range)
#    # Perform the inverse Fourier transform to obtain the filtered signal
#    filtered_signal = np.fft.ifft(np.fft.ifftshift(filtered_signal_fft))
#    return filtered_signal

#def filter_frequencies_range_incl(freqs, sign_fft, freqs_range):
#    logger = logging.getLogger(__name__)
#    range_tokens = freqs_range.split(',')
#    range_len = len(range_tokens)
#    logger.info('  Filtering for range: ' + freqs_range + ' (tokens: ' + str(range_len) + ')')
#    try:
#        if (len(freqs_range) > 1):
#            freq_low = (range_tokens[0]).strip()
#            freq_high = (range_tokens[1]).strip()
#            low_is_minus_infinite = (freq_low == '')
#            high_is_infinite = (freq_high == '')
#            both_infinite = low_is_minus_infinite and high_is_infinite
#            logger.info('    low:  ' + str(freq_low) + ' (-infinite: ' + str(low_is_minus_infinite) + ')')
#            logger.info('    high: ' + str(freq_high) + ' (+infinite: ' + str(high_is_infinite) + ')')
#            # Define the frequency range
#            # Create a frequency mask to include the specified range
#            if (not both_infinite):
#                if (low_is_minus_infinite):
#                    logger.info('    Range is open to the LEFT')
#                    freq_mask = (np.abs(freqs) > float(freq_high))
#                else:
#                    if (high_is_infinite):
#                        logger.info('    Range is open to the RIGHT')
#                        freq_mask = (np.abs(freqs) < float(freq_low))
#                    else:
#                        logger.info('    Range is CLOSED')
#                        freq_mask = (np.abs(freqs) < float(freq_low)) | (np.abs(freqs) > float(freq_high))
#                # Apply the mask to the Fourier transform
#                sign_fft[freq_mask] = 0  # Set the frequencies outside the range to zero
#    except Exception as e:
#        logger.warning('Filtering range ' + freqs_range + ' resulted in errors (' + str(e) + ') and will be skipped')
#        #logger.exception('Filtering range ' + freqs_range + ' resulted in errors (' + str(e) + ') and will be skipped')
#    return sign_fft
