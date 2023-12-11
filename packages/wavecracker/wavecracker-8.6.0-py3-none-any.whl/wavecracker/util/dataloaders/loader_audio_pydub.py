# v. 5.3.0 231111

import logging
import numpy as np

from config_util import get_audio_constants
from common_dataload_util import build_audio_channelsets, get_audio_channels #, eval_audio_time_vals
from multichannel_util import load_inmemory_table

def get_sep_pydchannel(channels, startv, stepv):
    if (startv > 0):
        chann = channels[startv::stepv]
    else:
        chann = channels[::stepv]
    return chann

def load_raw_audio(root_cfg, loading_cfg, attempt_idx, options_dictionary, dfile_path, audiofile_type):
    logger = logging.getLogger(__name__)
    loader_type = 'audio'
    audio_channelsets = []
    samples_count_ok = True # only one time axis, in an audio file should be always true
    logger.info('[' + str(attempt_idx) + '] Dataset ingestion attempt #' + str(attempt_idx) + ' ongoing (type: ' + loader_type + ', subtype: ' + audiofile_type + ', file: ' + dfile_path + ')')
    num_samples = 0

    # I could have hardcoded as pydub 
    # does not do anything that has a x-axis different from time.
    x_field, x_file_token = get_audio_constants(root_cfg)
    #print('pydub ------------------------------------ get_audio_constants rest anche filetoken per T')
    y_field_dict_key = 'yname'
    common_signal_step = 2
    left_idx_s, right_idx_s = 0, 1

    try:
        from pydub import AudioSegment
    except ImportError as ie:
        lib_token_str = 'pydub'
        logger.error('[' + str(attempt_idx) + '] Module \'' + lib_token_str + '\' cannot be loaded (error message was: ' + str(ie) + '). Impact: ' + lib_token_str + '-based data loader for some audio files is DISABLED')
    else:
        #extract audio
        audio_contents = AudioSegment.from_file(dfile_path, format=audiofile_type)

        # Convert to numpy array
        signal_sound_array = np.array(audio_contents.get_array_of_samples())
        logger.debug('[' + str(attempt_idx) + '] Signal values mp array built')

        audio_channels_count = audio_contents.channels
        # Extract left and right channel samples
        signal_snd_arr_L = get_sep_pydchannel(signal_sound_array, left_idx_s, common_signal_step) # signal_sound_array[::2]
        signal_snd_arr_R = None
        if (audio_channels_count > 1):
            signal_snd_arr_R = get_sep_pydchannel(signal_sound_array, right_idx_s, common_signal_step) # signal_sound_array[1::2]

        chann_dictionaries, sign_is_mono, is_left_chosen, is_interleaved_chosen = get_audio_channels(attempt_idx, options_dictionary, signal_snd_arr_L, signal_snd_arr_R, audio_channels_count, left_idx_s, right_idx_s)
        num_channels_ret = len(chann_dictionaries)
        summ_log = '[' + str(attempt_idx) + '] Audio channels collected: ' + str(num_channels_ret)
        if (not (num_channels_ret > 0)):
            logger.warn(summ_log)
        else:
            summ_log = summ_log + ' [' + ', '.join([d[y_field_dict_key] for d in chann_dictionaries]) + ']'
            logger.info(summ_log)

            # chann_dictionaries is an array of dictionaries:
            # [
            #   {
            #     'yname': xxxx,
            #     'audiodata': ....,
            #     'filetoken': ...
            #   },
            #   {
            #     'yname': xxxx,
            #     'audiodata': ....,
            #     'filetoken': ...
            #   }
            # ]

            frame_rate = audio_contents.frame_rate
            logger.debug('[' + str(attempt_idx) + '] Frame rate retrieved: ' + str(frame_rate))

            samples_count_ok, audio_channelsets = build_audio_channelsets(attempt_idx, chann_dictionaries, x_field, x_file_token, frame_rate)
            #logger.debug('\n\n[' + str(attempt_idx) + '] Num. of samples: ' + str(num_samples))

    return samples_count_ok, audio_channelsets



