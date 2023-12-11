# v. 7.2.1 231118

##### diagnostics-related imports - begin
import importlib
import datetime
from importlib.metadata import version as pkg_dist_version
import os
import sys
import subprocess
from common_util import get_exe_version, getFFMPEGVersCommandParams
##### diagnostics-related imports - end

def boot_checks():
    ################# DIAGNOSTICS MODULE - BEGIN - BY ARCHITECTURE IT MUST NOT USE FUNCTIONS DEFINED ELSEWHERE
    ################# ALSO IT MUST USE THE LOWEST AMOUNT OF DEPENDENCIES POSSIBLE
    ################# Not even the logging, nothing
    diag_var = 'SA_DIAG'
    diagnost_on = (os.environ[diag_var] if diag_var in os.environ else 'off').lower() in ['on', 'true']

    startup_log(diagnost_on, 'INFO', 'Checking dependencies ...')
    #crit_deps_var='SA_DEPS_CRIT'
    #opt_deps_var='SA_DEPS_OPT'
    crit_depts='yaml,numpy,pandas,chardet,scipy,matplotlib,tkinter'
    opt_depts='psutil,pydub,moviepy,pywt'
    #critical_unavails, c_count = get_unavails(diag_on, os.environ[crit_deps_var] if crit_deps_var in os.environ else None, 'critical')
    #opt_unavails, o_count = get_unavails(diag_on, os.environ[opt_deps_var] if opt_deps_var in os.environ else None, 'optional')
    critical_unavails, c_count = get_unavails(diagnost_on, crit_depts, 'critical')
    opt_unavails, o_count = get_unavails(diagnost_on, opt_depts, 'optional')

    native_opt_depts=[getFFMPEGVersCommandParams()]
    opt_native_unavails, eo_count = get_native_unavails(diagnost_on, native_opt_depts, 'optional')

    if (eo_count > 0):
        startup_log(diagnost_on, 'WARN', 'Missing optional native modules (' + str(eo_count) + '): ' + ', '.join(opt_native_unavails))
    if (o_count > 0):
        startup_log(diagnost_on, 'WARN', 'Missing optional dependencies (' + str(o_count) + '): ' + ', '.join(opt_unavails))
    if (c_count > 0):
        startup_log(diagnost_on, 'CRITICAL', 'ABORT. Missing ***REQUIRED*** dependencies (' + str(c_count) + '): ' + ', '.join(critical_unavails))
        startup_log(diagnost_on, 'CRITICAL', 'Ref. guidelines in the setup documentation')
        sys.exit(1)
    return diagnost_on
    ################# DIAGNOSTICS SECTION - END - BY ARCHITECTURE IT MUST NOT USE FUNCTIONS DEFINED ELSEWHERE

def startup_log(diag_on, level_s, s):
    level = level_s.strip().upper() if level_s else 'DEBUG'
    current_time = datetime.datetime.now()
    if (diag_on) or (level in ['WARN', 'ERROR', 'CRITICAL']):
        print('[' + current_time.strftime("%Y-%m-%d %H:%M:%S") + '][BOOT][' + level + '] ' + s)

def get_distr_ver(diag_on, pkg_name):
    try:
        to_ret = pkg_dist_version(pkg_name)
    except Exception as error:
        to_ret = 'version: na'
        startup_log(diag_on, 'DEBUG', 'Minor error while retrieving ' + pkg_name + ' distribution version: ' + str(error))
    return to_ret

def import_mod(diag_on, mod_n):
    h_module = importlib.import_module(mod_n)
    #does not work: getattr(mod_n, '__version__', 'n. a.')
    return get_distr_ver(diag_on, mod_n)

def get_unavails(diag_on, mod_list, dep_type):
    unavails = []
    for module_n in ([] if (mod_list is None) else mod_list.split(',')):
        try:
            mod_ver = import_mod(diag_on, module_n)
            startup_log(diag_on, 'INFO', '[dependency (py)] ' + module_n + ': OK (' + mod_ver + ')')
        except Exception as e:
            #startup_log(diag_on, 'CRITICAL', '[dependency (py)] ' + module_n + ': KO (' + str(e) + ')')
            unavails.append(module_n)
    return unavails, len(unavails)

#def get_native_ver(native_name, ver_command_n):
#    ver_ret = 'n.a.'
#    #try:
#    result = subprocess.run(ver_command_n, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#    status_code = result.returncode
#    if (status_code == 0):
#        #output_lines = result.stdout.split('\n')[:1]
#        #ver_ret = output_lines[0]
#        ver_ret = result.stdout.split('\n')[0]
#    else:
#        raise Exception(native_name + ': not found')
#    return ver_ret

def get_native_unavails(diag_on, native_list, dep_type):
    unavails = []
    for native_n in ([] if (native_list is None) else native_list):
        try:
            native_name, n_ver_command, n_linestotake = native_n[0], native_n[1], native_n[2]
            #native_ver = get_native_ver(native_name, n_ver_command)
            native_ver = get_exe_version(None, native_name, n_ver_command, n_linestotake, True)
            startup_log(diag_on, 'INFO', '[dependency (native)] ' + native_name + ': OK (' + native_ver + ')')
        except Exception as e:
            unavails.append(native_name)
    return unavails, len(unavails)
