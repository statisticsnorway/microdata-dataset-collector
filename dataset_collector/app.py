import logging
import sys
import threading
import time
import uuid

import json_logging

from dataset_collector.adapter import job_service_client
from dataset_collector.config import environment
from dataset_collector.decrypt import decrypt_service


def init_json_logging():
    json_logging.CREATE_CORRELATION_ID_IF_NOT_EXISTS = True
    json_logging.CORRELATION_ID_GENERATOR = (
        lambda: "dataset-collector-" + str(uuid.uuid1())
    )


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

RUN_JOB_SERVICE_CLIENT = environment.get('RUN_JOB_SERVICE_CLIENT')


def main():
    init_json_logging()

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
