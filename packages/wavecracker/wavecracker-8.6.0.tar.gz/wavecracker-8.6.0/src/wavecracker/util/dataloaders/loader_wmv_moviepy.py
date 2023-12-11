# v. 5.3.0 231111

from config_util import get_audio_constants
import logging
import numpy as np
#import sys

from common_dataload_util import build_audio_channelsets, get_audio_channels, eval_audio_time_vals

def close_mediaclip_wm(attempt_idx, vclip):
    logger = logging.getLogger(__name__)
    if (not (vclip is None)):
        try:
            vclip.close()
            #vclip.reader.close_proc()
            logger.debug('[' + str(attempt_idx) + '] Moviepy media clip closed')
        except ImportError as ie:
            logger.warn('Minor error, mediaclip could not be closed (' + str(ie) + ')')
# the .close prevented this from happening at the end of the program, in case I would not collect any channel
# (ie hardcoding num_channels = 0 in line 117 below - casually discovered just by testing)
#	Exception ignored in: <function FFMPEG_VideoReader.__del__ at 0x000002890ACD5800>
# Traceback (most recent call last):
#  File "......\Python311\Lib\site-packages\moviepy\video\io\ffmpeg_reader.py", line 199, in __del__
#    self.close()
#  File ".......\Python311\Lib\site-packages\moviepy\video\io\ffmpeg_reader.py", line 190, in close
#    self.proc.terminate()
#  File ".......\Python311\Lib\subprocess.py", line 1642, in terminate
#    _winapi.TerminateProcess(self._handle, 1)
#OSError: [WinError 6] Handle non valido

def load_raw_wmv_mpy(root_cfg, loading_cfg, attempt_idx, options_dictionary, dfile_path):
    logger = logging.getLogger(__name__)
    loader_type = 'audio'
    audiofile_type = 'wmv'
    y_field_dict_key = 'yname'
    left_audio_indx, right_audio_indx = 0, 1
    samples_count_ok = True # only one time axis, in an audio file should be always true
    time_vals, signal_vals, num_samples = None, None, 0
    audio_channelsets = []

    x_field, x_filetoken = get_audio_constants(root_cfg)

    video_clip = None
    logger.info('[' + str(attempt_idx) + '] Dataset ingestion attempt #' + str(attempt_idx) + ' ongoing (type: ' + loader_type + ', subtype: ' + audiofile_type + ', file: ' + dfile_path + ')')
    #logger.warn('[' + str(attempt_idx) + '] LOADER NOT IMPLEMENTED for this type (' + loader_type + ')')
    # Load video file
    try:
        from moviepy.editor import VideoFileClip #pip install moviepy
    except ImportError as ie:
        lib_token_str = 'moviepy'
        logger.error('[' + str(attempt_idx) + '] Module \'' + lib_token_str + '\' cannot be loaded (error message was: ' + str(ie) + '). Impact: ' + lib_token_str + '-based data loader for some audio files (' + audiofile_type + ') is DISABLED')
    else:
        # Extract audio
        video_clip = VideoFileClip(dfile_path)
        audio_contents = video_clip.audio

        #thresh_py_ver = 'x.y.z'
        #thr_major, thr_minor, thr_micro = map(int, thresh_py_ver.split('.'))
        #is_new = sys.version_info >= (thr_major, thr_minor, thr_micro)
        #logger.warning('[' + str(attempt_idx) + '] - PYTHON VERSION: ' + sys.version)
        #if (is_new):
        thresh_py_ver = '3.12.0'
        try:
            # Convert to numpy array and eval num channels
            # works with    python 3.1.2 (3.12.0), moviepy 1.0.3, numpy 1.26.1
            # AND also with python 3.1.1 (3.11.3), moviepy 1.0.3, numpy 1.23.5
            logger.debug('[' + str(attempt_idx) + '] >=' + thresh_py_ver + ' WAY - BEGIN')
            audio_array = np.array(list(audio_contents.iter_frames()))
            audio_channels_count = audio_array.shape[1] if audio_array.ndim > 1 else 1
            signal_sound_array = audio_array.reshape(-1, audio_channels_count)
            logger.debug('[' + str(attempt_idx) + '] >=' + thresh_py_ver + ' WAY - END')
        except Exception as e:
            logger.warning('[' + str(attempt_idx) + '][' + __file__ + '] Minor error while converting stream to sound array (' + str(e) + '), attempting strategy #2 ..')
            logger.debug('[' + str(attempt_idx) + '] <' + thresh_py_ver + ' WAY - BEGIN')
            # Convert to numpy array and eval num channels
            # works with python 3.1.1 (3.11.3), moviepy 1.0.3, numpy 1.23.5 (just in case the strategy above didn't work)
            logger.debug('[' + str(attempt_idx) + '] <' + thresh_py_ver + ' WAY - BEGIN')
            signal_sound_array = audio_contents.to_soundarray()
            audio_channels_count = signal_sound_array.ndim
            logger.debug('[' + str(attempt_idx) + '] Signal values mp array built')

        signal_snd_arr_L = signal_sound_array[:, left_audio_indx]
        signal_snd_arr_R = None
        if (audio_channels_count > 1):
           signal_snd_arr_R = signal_sound_array[:, right_audio_indx]

        chann_dictionaries, sign_is_mono, is_left_chosen, is_interleaved_chosen = get_audio_channels(attempt_idx, options_dictionary, signal_snd_arr_L, signal_snd_arr_R, audio_channels_count, left_audio_indx, right_audio_indx)
        num_channels_ret = len(chann_dictionaries)
        summ_log = '[' + str(attempt_idx) + '] Audio channels collected: ' + str(num_channels_ret)
        if (not (num_channels_ret > 0)):
            logger.warn(summ_log)
        else:
            summ_log = summ_log + ' [' + ', '.join([d[y_field_dict_key] for d in chann_dictionaries]) + ']'
            logger.info(summ_log)

            frame_rate = audio_contents.fps
            logger.debug('[' + str(attempt_idx) + '] Frame rate retrieved: ' + str(frame_rate))

            samples_count_ok, audio_channelsets = build_audio_channelsets(attempt_idx, chann_dictionaries, x_field, x_filetoken, frame_rate)
            #logger.debug('\n\n[' + str(attempt_idx) + '] Num. of samples: ' + str(num_samples))

    close_mediaclip_wm(attempt_idx, video_clip)

    return samples_count_ok, audio_channelsets
