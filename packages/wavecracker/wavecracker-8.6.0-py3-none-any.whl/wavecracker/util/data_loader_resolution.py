# v. 2.1.0 231101

import logging
from config_util import get_loader_override, get_loader_by_ext
from file_util import get_file_basename_and_ext
from loader_csv_1 import load_raw_csv_1
from loader_mp3_pydub import load_raw_mp3_pyd
from loader_mp4_pydub import load_raw_mp4_pyd
from loader_wav_pydub import load_raw_wav_pyd
from loader_wmv_moviepy import load_raw_wmv_mpy

def resolve_loader_func(config, loading_config, filepath):
    logger = logging.getLogger(__name__)
    loader_func_override = get_loader_override(loading_config)
    is_overridden = not (loader_func_override is None)
    resolut_failure = False
    _, f_extension = get_file_basename_and_ext(filepath)
    if (is_overridden):
        loader_func_name = loader_func_override
        logger.debug('Loader function name resolved by override: >' + loader_func_name + '<')
    else:
        loader_func_name = get_loader_by_ext(config, f_extension)
        logger.debug('Loader function name inferred: >' + loader_func_name + '<')

    try:
        loader_function = globals()[loader_func_name]
    except Exception as e:
        logger.warn('Data loader function resolution failed (msg: ' + str(e) + '), remediation will take place, but it is recommended to check configuration')
        resolut_failure = True
        hdef_loader_function = load_raw_csv_1
        if (is_overridden):
            try:
                logger.warn('Data loader function resolution will be attempted by inferring it (as it was first attempted by override with ' + loader_func_override + ')')
                loader_func_name = get_loader_by_ext(config, f_extension)
                loader_function = globals()[loader_func_name]
            except Exception as e:
                loader_function = hdef_loader_function
                logger.warn('Data loader function could not be inferred (msg: ' + str(e) + '); resolution will be made by hard default, but configuration should be checked')
        else:
            loader_function = hdef_loader_function
            logger.warn('Data loader function resolution will be made by hard default')

    loader_name_as_created = loader_function.__name__
    return loader_function, loader_name_as_created, is_overridden, resolut_failure

