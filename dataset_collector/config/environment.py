import os


def _initialize_environment() -> dict:
    return {
        'RSA_KEY_DIR': os.environ['RSA_KEY_DIR'],
        'ENCRYPTED_DIR': os.environ['ENCRYPTED_DIR'],
        'DECRYPTED_DIR': os.environ['DECRYPTED_DIR'],
        'JOB_SERVICE_URL': os.environ['JOB_SERVICE_URL'],
        'RUN_JOB_SERVICE_CLIENT': os.environ['RUN_JOB_SERVICE_CLIENT'],
        'DOCKER_HOST_NAME': os.environ['DOCKER_HOST_NAME']
    }


_ENVIRONMENT_VARIABLES = _initialize_environment()


def get(key: str) -> str:
    return _ENVIRONMENT_VARIABLES[key]
