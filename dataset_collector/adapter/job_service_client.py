import json
import logging
import os
from typing import List

import requests
from requests import RequestException

from dataset_collector.exception import HttpRequestError, HttpResponseError

logger = logging.getLogger()

JOB_SERVICE_URL = os.environ['JOB_SERVICE_URL']

IMPORTABLE_DATASETS_URL = f'{JOB_SERVICE_URL}/importable-datasets'
JOBS_URL = f'{JOB_SERVICE_URL}/jobs'


def __create_jobs() -> List:
    try:
        response = requests.get(IMPORTABLE_DATASETS_URL).json()
    except RequestException as e:
        logger.exception(e)
        raise HttpRequestError(e) from e

    jobs = []
    if len(response) > 0:
        logger.info(f'Importable datasets: {json.dumps(response, indent=2)}')
        for dataset in response:
            if dataset["hasMetadata"] and dataset["hasData"]:
                jobs.append({"operation": "ADD", "target": dataset["datasetName"]})
        logger.info(f'Jobs to submit: {json.dumps(jobs, indent=2)}')

    return jobs


def __import_request(jobs: List):
    try:
        response = requests.post(JOBS_URL, headers={"Content-Type": "application/json"}, json={"jobs": jobs})
    except RequestException as e:
        logger.exception(e)
        raise HttpRequestError(e) from e
    if response.status_code != 200:
        raise HttpResponseError(f'{response.text}')

    logger.info(f'Response: {json.dumps(response.json(), indent=2)}')


def import_datasets():
    __import_request(__create_jobs())
