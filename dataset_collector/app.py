import logging
import threading
import time

from dataset_collector.adapter import job_service_client
from dataset_collector.decrypt import decrypt_service
from dataset_collector.config import environment

logger = logging.getLogger()

RUN_JOB_SERVICE_CLIENT = environment.get('RUN_JOB_SERVICE_CLIENT')


def main():
    log_thread = threading.Thread()
    log_thread.start()

    try:
        while True:
            time.sleep(10)

            decrypt_service.decrypt()
            if RUN_JOB_SERVICE_CLIENT:
                job_service_client.import_datasets()
    except Exception as exc:
        logger.exception('Service stopped by exception', exc_info=exc)


if __name__ == '__main__':
    logger.info('Polling for encrypted files...')
    main()
