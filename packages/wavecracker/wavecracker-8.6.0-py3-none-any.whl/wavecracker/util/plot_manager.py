# v. 8.6.0 231210

import numpy as np
#import matplotlib.pyplot as pXlt
#from matplotlib.ticker import FuncFormatter
#from scipy.signal import welch

from plot_window_wrap import PlotWindowWrapper
from config_util import get_freq_xgrain, get_rainbow_colors, get_polynt_params
from file_util import get_file_basename

from plot_util import common_axes_personalization, override_axis_boundaries #, eval_subplot_title
from plot_origsignal import addplot_orig_sign
from plot_ft import addplot_ft
from plot_ftphase import addplot_ftphase
from plot_psd import addplot_psd
from plot_histogram import addplot_histogram
from plot_spectrogram import addplot_spectrogram
from plot_3d_spectrogram import addplot_3d_spectrogram
from plot_wavelet import addplot_wavelet
from plot_wavelet import addplot_wavelet
from plot_qq import addplot_qq_sign
from plot_instfreq import addplot_instfreq

#import pywt

import logging

class PlotsBuilder:
    def __init__(self, is_multitab, dedic_tabs, config_hnd, channset_name, chann_xfield, chann_yfield, orig_xlbl, orig_ylbl, chann_name, origsubplot_type_label, incl_original, incl_four_transf, src_info, num_samples_pre, num_samples, num_freq_vals, samp_freq, remove_dc_offset, time_values, time_boundaries, signal_values, sign_peaks_vals, signal_filtered_values, frequencies_values, signal_fft_magn_vals, ft_magn_boundaries, plot_signal_ampl_window, plot_ft_freq_window, sig_ft_phase, psd_freq_window, psd_pow_boundaries, hist_val_window, hist_freq_window, ftphase_freq_window, ftphase_val_window, incl_spectrogr, incl_3dspectrogr, incl_hist, psd_x_axis_vals, psd_y_axis_vals, wavl_scales, wavl_transf_data, wv_type, include_qq, poly_int_data, inst_freq):

        self.multi_tab = is_multitab
        self.dedicated_tabs = dedic_tabs
        self.incl_orig = incl_original
        self.orig_xlbl = orig_xlbl
        self.orig_ylbl = orig_ylbl
        self.incl_ft = incl_four_transf
        self.incl_qq = include_qq
        self.instant_freq = inst_freq

        self.polynt_scopes = poly_int_data

        self.channelset_name = channset_name
        self.channel_xfield = chann_xfield
        self.channel_yfield = chann_yfield
        self.channel_name = chann_name
        self.orig_splot_type_lab = origsubplot_type_label

        self.source_info = get_file_basename(src_info) if (not (src_info is None)) else 'source: unknown'
        self.time = time_values

        self.num_time_samples_pre = num_samples_pre
        self.num_time_samples = num_samples
        self.downsampled = (not (num_samples_pre is None)) and (num_samples < num_samples_pre)
        #self.downsampled = num_samples > num_samples_pre

        self.num_freq_values = num_freq_vals
        self.signal = signal_values
        self.signal_peaks = sign_peaks_vals
        self.signal_filtered = signal_filtered_values
        self.frequencies = frequencies_values
        #self.signal_fft = signal_fft_values
        self.signal_fft_magnitude = signal_fft_magn_vals
        self.signal_ft_phase = sig_ft_phase
        self.config = config_hnd

        self.sig_time_window = time_boundaries
        self.sig_ampl_limits = plot_signal_ampl_window

        self.ft_freq_limits = plot_ft_freq_window
        self.ft_magn_limits = ft_magn_boundaries

        self.psd_x_vals = psd_x_axis_vals
        self.psd_y_vals = psd_y_axis_vals
        self.psd_freq_limits = psd_freq_window
        self.psd_pow_limits = psd_pow_boundaries

        self.hist_val_limits = hist_val_window
        self.hist_freq_limits = hist_freq_window

        self.ftphase_freq_limits = ftphase_freq_window
        self.ftphase_val_limits = ftphase_val_window

        self.wv_scales = wavl_scales
        self.wavelet_transform_data = wavl_transf_data
        self.wavelet_type = wv_type

        self.sampling_freq = samp_freq
        self.dc_offset_suppressed = remove_dc_offset
        self.include_spectrogram = incl_spectrogr
        self.include_3dspectrogram = incl_3dspectrogr
        #self.plXt_hnd = None
        self.plotWindowWrap = None
        #self.incl_envelope = incl_envelope
        #self.incl_psd = incl_psd
        self.incl_hist = incl_hist
        #self.include_wavelet = incl_wavelet

    def createPlots(self):
        logger = logging.getLogger(__name__)

        num_subplots = 0;
        #self.pXlt_hnd = None

        # init subplots dictionary
        subplots_dict = {} # ket: file suffix for split saving; value: subplot axes

        rainbow_string = get_rainbow_colors(self.config)
        rainbow_colors = rainbow_string.split(',')

        include_sig_filtered = not (self.signal_filtered is None)
        incl_envelope = not (self.signal_peaks is None)

        include_phasepl = not (self.signal_ft_phase is None)
        incl_psd = not ((self.psd_x_vals is None) or (self.psd_y_vals is None))
        include_wavelet = not ((self.wv_scales is None) or (self.wavelet_transform_data is None))

        include_inst_freq = not (self.instant_freq is None)

        if (self.incl_orig):
            num_subplots = num_subplots + 1;
        if (self.incl_ft):
            num_subplots = num_subplots + 1;
        if (include_wavelet):
            num_subplots = num_subplots + 1;
        if (self.include_3dspectrogram):
            num_subplots = num_subplots + 1;
        if (self.include_spectrogram):
            num_subplots = num_subplots + 1;
        if (incl_psd):
            num_subplots = num_subplots + 1;
        if (self.incl_hist):
            num_subplots = num_subplots + 1;
        if (include_phasepl):
            num_subplots = num_subplots + 1;
        if (self.incl_qq):
            num_subplots = num_subplots + 1;
        if (include_inst_freq):
            num_subplots = num_subplots + 1;

        orig_xlabel, orig_ylabel = self.orig_xlbl, self.orig_ylbl

        any_polynt = (len(self.polynt_scopes) > 0)

        if (any_polynt):
            num_subplots = num_subplots + len(self.polynt_scopes);

        if (num_subplots > 0):
            logger.info('Creating plots ...')

            #self.plotWindowWrap = PlotWindowWrapper(self.multi_tab, self.config, self.downsampled, self.num_time_samples_pre, self.num_time_samples, self.num_freq_values, num_subplots, self.source_info)
            self.plotWindowWrap = PlotWindowWrapper(self.multi_tab, self.config, num_subplots, self.source_info)
            #post_dssampl_subplot_title = '' if (not self.downsampled) else ' (downsampled, ' + str(self.num_time_samples_pre) + '-->' + str(self.num_time_samples) + ')'
            # Plot the Original Signal

            #self.downsampled, self.num_time_samples_pre, self.num_time_samples
            if (self.incl_orig):
                tab_title = 'Signal (orig.)'
                plot_dict_key = 'orig'
                opdesc = tab_title
                plot_title = self.channel_name + ' (' + self.orig_splot_type_lab + ')'
                #plot_title = #eval_subplot_title(self.channelset_name, self.channel_xfield, self.channel_yfield, self.channel_name, self.orig_splot_type_lab)
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                # first opdesc (in logs), then plot_title (in subplot_title); typically, it's fine to have them identical
                #addplot_orig_sign addplot_qq_sign
                o_xlabel = orig_xlabel + ' (downsampled: ' + str(self.num_time_samples_pre) + ' ->' + str(self.num_time_samples) + ')' if (self.downsampled) else orig_xlabel + ' ('+str(self.num_time_samples)+' samples)'
                addplot_orig_sign(self.config, opdesc, o_xlabel, self.channelset_name, orig_ylabel, plot_title, targetAxes, self.time, self.signal, self.sig_time_window, self.sig_ampl_limits,
                                  incl_envelope, self.signal_peaks, include_sig_filtered, self.signal_filtered)
                subplots_dict[plot_dict_key] = targetAxes

                if (any_polynt):
                    polint_idx = 0
                    polynt_color, polynt_lstyle, polynt_lwid, coeff_short_fmt = get_polynt_params(self.config) 
                    for polint_scope in self.polynt_scopes:
                        polint_idx = polint_idx + 1
                        nsliced_samples, pdegree, mask_low, mask_hi, coeffs, sliced_time, sliced_signal, interpolated_signal = polint_scope
                        tab_title = 'Polyfit #' + str(polint_idx) + ' (' + str (pdegree) + ')'
                        plot_dict_key = 'orig-polint-' + str(polint_idx)
                        opdesc = tab_title
                        plot_title = self.channel_name + ' (' + self.orig_splot_type_lab + '+poly' + str(pdegree) + ')'
                        isDedicatedTab = plot_dict_key in self.dedicated_tabs
                        coeffs_as_str = '\n(coeffs: ' + ', '.join([format(c, coeff_short_fmt) for c in coeffs]) + ')' if (pdegree < 5) else '\n(coeffs: ref. log)'
                        op_xlabel = orig_xlabel + ' [' + str(mask_low) + '-' + str(mask_hi) + ']' + coeffs_as_str
                        targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                        addplot_orig_sign(self.config, opdesc + ' (orig slice)', None, None, None, None, targetAxes, sliced_time, sliced_signal,
                                      None, None, None, None, None, None)
                        addplot_orig_sign(self.config, opdesc + ' (polyint slice)', op_xlabel, self.channelset_name, orig_ylabel, plot_title, targetAxes, sliced_time, interpolated_signal,
                                      None, None, False, None, None, None, polynt_color, polynt_lstyle, polynt_lwid, '+poly' + str(pdegree))
                        subplots_dict[plot_dict_key] = targetAxes

            #### applies to ALL plots having frequency in the x-axis, except the wavelet transform
            frequency_grain = get_freq_xgrain(self.config)
            logger.debug('frequency grain set: ' + str(frequency_grain))

            # Plot the Fourier transform
            if (self.incl_ft):
                tab_title = 'Fourier tr.'
                plot_dict_key = 'ft'
                opdesc = 'Fourier transform'
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_ft(self.config, opdesc, targetAxes, self.frequencies, self.signal_fft_magnitude, frequency_grain, self.ft_freq_limits, self.ft_magn_limits, self.dc_offset_suppressed)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the QQ Plot
            if (self.incl_qq):
                tab_title = 'Q-Q'
                plot_dict_key = 'qq'
                opdesc = tab_title
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_qq_sign(self.config, opdesc, orig_ylabel, targetAxes, self.signal)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the istant. frequency Plot
            if (include_inst_freq):
                tab_title = 'Inst. Freq.'
                plot_dict_key = 'if'
                opdesc = tab_title
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                #addplot_instfreq(self.config, opdesc, orig_ylabel, targetAxes, self.time, self.signal, self.instant_freq)
                addplot_instfreq(self.config, opdesc, orig_xlabel, orig_ylabel, targetAxes, self.time, self.signal, self.instant_freq, self.sig_time_window, self.sig_ampl_limits)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the PSD
            if (incl_psd):
                tab_title = 'PSD'
                plot_dict_key = 'psd'
                opdesc = tab_title
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_psd(self.config, opdesc, targetAxes, self.psd_x_vals, self.psd_y_vals, frequency_grain, self.psd_freq_limits, self.psd_pow_limits, self.dc_offset_suppressed)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the values histogram
            if (self.incl_hist):
                tab_title = 'Histogram'
                plot_dict_key = 'hist'
                opdesc = 'Values histogram'
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_histogram(self.config, opdesc, targetAxes, self.signal, self.hist_val_limits, self.hist_freq_limits, rainbow_colors)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the phase plot
            if (include_phasepl):
                tab_title = 'Fourier tr. (ph.)'
                plot_dict_key = 'ft-phase'
                opdesc = 'Fourier transform phase'
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_ftphase(self.config, opdesc, targetAxes, self.frequencies, self.signal_ft_phase, frequency_grain, self.ftphase_freq_limits, self.ftphase_val_limits)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the wavelet transform plot
            if (include_wavelet):
                tab_title = 'Wavelet tr.'
                plot_dict_key = 'wvlet'
                opdesc = 'Wavelet transform'
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_wavelet(self.config, opdesc, targetAxes, orig_xlabel, self.time, self.wv_scales, self.wavelet_transform_data, self.wavelet_type)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the 3d spectrogram plot
            if (self.include_3dspectrogram):
                tab_title = '3D Spectrogram'
                plot_dict_key = '3dspctg'
                opdesc = tab_title
                is3D = True
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, is3D, isDedicatedTab)
                addplot_3d_spectrogram(self.config, opdesc, targetAxes, orig_xlabel, self.sampling_freq, self.time, self.signal)
                subplots_dict[plot_dict_key] = targetAxes

            # Plot the spectrogram plot
            if (self.include_spectrogram):
                tab_title = 'Spectrogram'
                plot_dict_key = 'spctg'
                opdesc = tab_title
                isDedicatedTab = plot_dict_key in self.dedicated_tabs
                targetAxes = self.plotWindowWrap.nextsubplot_axes(tab_title, False, isDedicatedTab)
                addplot_spectrogram(self.config, opdesc, targetAxes, orig_xlabel, self.sampling_freq, self.time, self.signal)
                subplots_dict[plot_dict_key] = targetAxes

            self.plotWindowWrap.prepareForDisplay()

            logger.debug('Subplot dictionary entries: ' + str(len(subplots_dict)) + ', keys: ' + ', '.join(subplots_dict.keys()))
        else:
            logger.info('No plots created (per user request)')

        return subplots_dict

    def showPlots(self):
        logger = logging.getLogger(__name__)
        if (self.plotWindowWrap):
            self.plotWindowWrap.showPlots()
