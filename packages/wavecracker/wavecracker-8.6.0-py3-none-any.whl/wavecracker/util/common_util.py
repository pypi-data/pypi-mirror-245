# v. 8.6.0 231210

import logging
import os
import subprocess
import platform
import socket
import sys
import signal
from datetime import datetime
from pprint import pformat
import site
from distutils.sysconfig import get_python_lib
from hw_diagnostics import show_hw_info

import random
import string

tool_name = 'Wave Cracker'
tool_ver='8.6.0'

def log_app_banner():
    global tool_name
    global tool_ver
    logger = logging.getLogger(__name__)
    logger.info(tool_name + ' v. ' + tool_ver + ' - BEGIN')

def debugRobust(logger, s):
    if (logger):
        logger.debug(s)
    #else:
    #    print('[DEBUG]' + s)

def warningRobust(logger, s):
    if (logger):
        logger.warning(s)
    #else:
    #    print('[WARN]' + s)

#tricks with logger needed as this may be called also BEFORE logging initialization
def get_exe_version(logger, exe_name, cmd_to_launch, version_token_index, raiseExcIfIssues):
    #logger = logging.getLogger(__name__)
    exe_version = 'n. a.'
    try:
        result = subprocess.run(cmd_to_launch, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout_str = result.stdout
        debugRobust(logger, 'Command output:\n' + str(stdout_str).replace('\n', '\n[stdout] '))
        output_lines = stdout_str.strip().split('\n')
        exe_version = output_lines[0].split(' ')[version_token_index]
    except subprocess.CalledProcessError as cpe:
        stderr_str = str(cpe.stderr).replace('\n', '\n[stderr] ')
        warningRobust(logger, '[w1] Failed to retrieve ' + exe_name + ' version (command was: >' + ' '.join(cmd_to_launch) + '<). Error output:%s', stderr_str)
    except Exception as ex:
        if(raiseExcIfIssues):
            raise Exception('module ' + exe_name + ' not found')
        else:
            warningRobust(logger, '[w2] Failed to retrieve ' + exe_name + ' version (command was: >' + ' '.join(cmd_to_launch) + '<): ' + str(ex))
    return exe_version

def getFFMPEGVersCommandParams():
    return 'ffmpeg', ['ffmpeg', '-version'], 2

def get_ffmpeg_version():
    logger = logging.getLogger(__name__)
    ffmpeg_cmd_params = getFFMPEGVersCommandParams()
    return get_exe_version(logger, ffmpeg_cmd_params[0], ffmpeg_cmd_params[1], ffmpeg_cmd_params[2], False)

def get_pip_version():
    logger = logging.getLogger(__name__)
    return get_exe_version(logger, 'pip', ['pip', '--version'], 1, False)

def print_host_diagnostics():
    logger = logging.getLogger(__name__)
    logger.info('Host: ' + socket.gethostname())
    show_hw_info()
    logger.info('OS: ' + platform.platform())
    logger.info('PID: ' + str(os.getpid()))
    logger.info('Python ver.: ' + sys.version)
    logger.info('Python home: ' + sys.prefix)
    pip_ver = get_pip_version()
    pip_ver and logger.info('PIP ver.: ' + pip_ver)
    ffmpeg_ver = get_ffmpeg_version()
    ffmpeg_ver and logger.info('FFMPEG ver.: ' + ffmpeg_ver)
    check_sitepackages()
    log_envvars(['PATH'])

def log_envvars(evars):
    logger = logging.getLogger(__name__)
    for cvar in evars:
        if ((cvar in os.environ) and (os.environ[cvar])):
            logger.info('env[' + cvar + ']: ' + os.environ[cvar])

def check_sitepackages():
    logger = logging.getLogger(__name__)
    # the [0] is the python home, which we know already
    #logger.info('site-packages (global)              : ' + site.getsitepackages()[1])
    logger.info('site-packages info : ' + str(site.getsitepackages()))
    logger.info('    - global : ' + str(site.getsitepackages()))
    logger.info('    - user   : ' + site.getusersitepackages())
    logger.info('    - current virtual env.: ' + get_python_lib())

def print_diagnostics(diagnost_on):
    logger = logging.getLogger(__name__)
    if (diagnost_on):
        print_host_diagnostics()

def os_ctrlc_handler(signum, frame):
    logger = logging.getLogger(__name__)
    logger.debug('OS Signal intercepted (signum: ' + str(signum) + ', frame: ' + str(frame) + ')')
    res = input('CTRL+C was pressed. Do you really want to exit? (y/n)')
    if res == 'y':
        exit(1)

def register_os_sig_handlers():
    logger = logging.getLogger(__name__)
    signal.signal(signal.SIGINT, os_ctrlc_handler)
    #signal.signal(signal.CTRL_BREAK_EVENT, os_ctrlc_handler)
    #signal.signal(signal.CTRL_C_EVENT, os_ctrlc_handler)
    logger.debug('OS Signal handler registered (signum: ' + str(signal.SIGINT) + ', handler: os_ctrlc_handler)')

#def remove_non_printable(text):
#    # Use a regular expression to remove non-printable characters
#    printable = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c")
#    return ''.join(filter(lambda x: x in printable, text))

def is_stdout_debug_on():
    env_variable_name = 'SA_DEBUG'
    return check_env_var(env_variable_name, ['on', 'true'], False)

def check_env_var(env_var, exp_values, case_sens):
    #print (os.environ[env_var])
    rc = ((env_var in os.environ) and ((os.environ[env_var] if case_sens else (os.environ[env_var]).lower()) in exp_values))
    return rc

def create_rnd_string(length, alphabet=None):
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def beautified_string(obj):
    if (obj is None):
        return 'None'
    else:
        pretty_string = pformat(obj)
        return pretty_string

def is_any_A_in_B(A, B):
    return (any(aelement in B for aelement in A))

def wrap_string(input_string, max_line_length, max_string_length):
    lines = []
    current_line = ''
    for word in input_string.split():
        if len(current_line) + len(word) + 1 <= max_line_length:
            # Add the word to the current line
            current_line += ' ' + word if current_line else word
        else:
            # Start a new line
            lines.append(current_line)
            current_line = word
    # Add the last line
    lines.append(current_line)
    #input_string = input_string_orig[:max_string_length]
    wrapped_string = '\n'.join(lines)
    if (len(wrapped_string) > max_string_length):
        wrapped_string = wrapped_string + '... (truncated)'
    return wrapped_string

#def insert_crlf(input_string, n):
#    return '\n'.join([input_string[i:i+n] for i in range(0, len(input_string), n)])

def get_formatted_tstamp(tformat):
    now = datetime.now()
    s_format = tformat if (not (tformat is None)) else '%Y%m%d%H%M%S%f' #yyyyMMddhhmisszzz
    formatted_tstamp = now.strftime(s_format)[:-3]
    return formatted_tstamp
