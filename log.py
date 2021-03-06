import datetime
import logging
import os

from config import get_main_configurations


def log(log_message):

    try:
        logger
    except NameError:
        startLogger()

    logger.info(log_message)

def startLogger():

    global logger

    logger = get_logger(
        format='%(asctime)s %(levelname)s %(message)s'
    )


def get_logger(format='%(asctime)s %(levelname)s %(threadName)s %(message)s',
               logfile=True,
               logout=True):


    now = datetime.datetime.now()

    home_dir = os.path.expanduser('~')
    log_dir_name = configs['log_directory']
    log_dir = "{}/{}".format(home_dir, log_dir_name)

    if not os.path.exists(log_dir):
        print 'creating log directory: {}'.format(log_dir)
        os.mkdir(log_dir)
        os.chmod(log_dir, 0777)

    log_dir_sub_dir = ["%s%02d"%(now.year, now.month)]
    for new_dir in log_dir_sub_dir:
        log_dir = "%s/%s/" % (log_dir, new_dir)
        if not os.path.exists(log_dir):
            print 'creating log directory: {}'.format(log_dir)
            os.mkdir(log_dir)
            os.chmod(log_dir, 0777)


    if not os.path.exists(log_dir):
        print 'creating log directory: {}'.format(log_dir)
        os.mkdir(log_dir)
        os.chmod(log_dir, 0777)

    log_path = os.path.join(
        log_dir, '{}_{}.log'.format(now.strftime('%Y%m%d_%H%M'),
                                    configs['log_name'])
    )
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(format)
   
    if logfile is True:
        print '{} logging to path: {}'.format(now, log_path)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    if logout is True:
        print 'logging to stdout'
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

configs = get_main_configurations()
