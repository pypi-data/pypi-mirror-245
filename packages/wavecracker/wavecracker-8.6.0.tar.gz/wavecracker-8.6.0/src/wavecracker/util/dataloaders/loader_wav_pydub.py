# v. 2.1.0 231101

import logging
from loader_audio_pydub import load_raw_audio

def load_raw_wav_pyd(root_cfg, loading_cfg, attempt_idx, options_dictionary, dfile_path):
    # audiostream_type, below, is NOT a file extension. DO NOT TOUCH IT, unless sure of what you are doing
    audiostream_type = 'wav'
    return load_raw_audio(root_cfg, loading_cfg, attempt_idx, options_dictionary, dfile_path, audiostream_type)
