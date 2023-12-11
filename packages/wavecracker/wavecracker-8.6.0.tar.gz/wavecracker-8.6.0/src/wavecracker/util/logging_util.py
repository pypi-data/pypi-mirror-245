# v. 4.3.0 231107

import datetime
import logging
import logging.config
import os

def init_logging(log_conf, logs_to_suppress):
    emerg_log_feat = 'STDOUT ONLY'
    try:
        if (os.path.exists(log_conf)):
            boot_log('INFO', 'Logging subsystem initialization (configuration: ' + log_conf + ') ...')
            logging.config.fileConfig(log_conf)
        else:
            boot_log('ERROR', 'Logging configuration file (' + log_conf + ') NOT FOUND. Switching to emergency logging system (' + emerg_log_feat + ')')
            init_emergency_log()
    except Exception as error:
        init_emergency_log()
        logger = logging.getLogger(__name__)
        logger.error('Logging subsystem initialization FAILED (error message: ' + str(error) + ', switching to emergency logging system (' + emerg_log_feat + ')')

    logger = logging.getLogger(__name__)
    #avoids log pollution with TONS of [PIL.TiffImagePlugin][DEBUG][TiffImagePlugin:915] 
    for cur_item in logs_to_suppress:
        logger.debug('Setting WARN level for logs of: ' + cur_item)       
        logging.getLogger(cur_item).setLevel(logging.WARNING)

def init_emergency_log():
    #basic_log_file='./logs/signal_analyzer.log'
    #logging.basicConfig(filename=basic_log_file,encoding='utf-8',level=logging.INFO, filemode = 'w', format='[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s') 
    logging.basicConfig(level=logging.INFO, encoding='utf-8', format='[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

def boot_log(level, s):
    current_time = datetime.datetime.now()
    # Format the timestamp as a string
    tstamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    #tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('[' + tstamp + '][BOOT][' + level + '] ' + s)
