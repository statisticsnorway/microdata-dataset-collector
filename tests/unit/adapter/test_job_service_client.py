import os

from requests_mock import Mocker as RequestsMocker

from dataset_collector.adapter import job_service_client

JOB_SERVICE_URL = os.environ['JOB_SERVICE_URL']

IMPORTABLE_DATASETS = [
    {'datasetName': 'DATASET_1', 'hasMetadata': True, 'hasData': True},
    {'datasetName': 'DATASET_2', 'hasMetadata': True, 'hasData': False},
    {'datasetName': 'DATASET_3', 'hasMetadata': True, 'hasData': True}
]


def test_create_jobs(requests_mock: RequestsMocker):
    requests_mock.get(
        f'{JOB_SERVICE_URL}/importable-datasets', json=IMPORTABLE_DATASETS
    )
    jobs = job_service_client.__create_jobs()

    assert len(jobs) == 2
    assert jobs[0] == {'operation': 'ADD', 'target': 'DATASET_1'}
    assert jobs[1] == {'operation': 'ADD', 'target': 'DATASET_3'}
