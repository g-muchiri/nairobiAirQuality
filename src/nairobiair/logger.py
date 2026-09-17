## A logger file is basically created to create a common configuration for logger object
import logging
import os

def nairobiAir_logger ():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ## Creating handlers if they dont exist
    if not logger.handlers:
        ##Confirm if there is an existing handler otherwise create
        current_dir= os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(current_dir,'..','logs')
        os.makedirs(logs_dir, exist_ok=True)

        log_file_path = os.path.join(logs_dir,'nairobiAir.logs')

        ##Create log and file handlers
        lh = logging.StreamHandler()
        lh.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)

        ##Creating formatter 
        format= logging.Formatter('%(asctime)s - %(levelname)s -%(name)s: %(message)s')

        lh.setFormatter(format)
        fh.setFormatter(format)

        logger.addHandler(fh)
        logger.addHandler(lh)

    return logger
        



