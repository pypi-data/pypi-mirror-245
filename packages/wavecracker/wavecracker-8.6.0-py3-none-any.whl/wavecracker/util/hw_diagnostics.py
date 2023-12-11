# v. 4.4.0 231109

import logging

def show_hw_info():
    logger = logging.getLogger(__name__)
    try:
        import psutil

        num_cpus = psutil.cpu_count(logical=False)  # physical CPUs
        num_lcpus = psutil.cpu_count(logical=True)  # logical CPUs
        logger.info('CPUs (phys/log): ' + str(num_cpus) + '/' + str(num_lcpus))

        disk_partitions = psutil.disk_partitions()
        logger.info('Disk Partitions: ' + str(disk_partitions))
        # Get information about disk usage
        disk_usage = psutil.disk_usage('/')
        logger.info('Disk Usage: ' + str(disk_usage))

        virtual_memory = psutil.virtual_memory()
        logger.info('Virtual Memory: ' + str(virtual_memory))
        swap_memory = psutil.swap_memory()
        logger.info('Swap Memory: ' + str(swap_memory))

        #show_cpuinfo()
        #show_memoryinfo()
        #show_volumesinfo()
    except Exception as e:
        logger.warn('Hardware diagnostics: not available; retrieval error: ' + str(e))

#def show_cpuinfo():
#    logger = logging.getLogger(__name__)
#    # Get the number of CPUs
#    num_cpus = psutil.cpu_count(logical=False)  # physical CPUs
#    num_lcpus = psutil.cpu_count(logical=True)  # logical CPUs
#    logger.info('CPUs (phys/log): ' + str(num_cpus) + '/' + str(num_lcpus))

#def show_volumesinfo():
#    logger = logging.getLogger(__name__)
#    disk_partitions = psutil.disk_partitions()
#    logger.info('Disk Partitions: ' + str(disk_partitions))
#    # Get information about disk usage
#    disk_usage = psutil.disk_usage('/')
#    logger.info('Disk Usage: ' + str(disk_usage))

#def show_memoryinfo():
#    logger = logging.getLogger(__name__)
#    virtual_memory = psutil.virtual_memory()
#    logger.info('Virtual Memory: ' + str(virtual_memory))
#    swap_memory = psutil.swap_memory()
#    logger.info('Swap Memory: ' + str(swap_memory))
