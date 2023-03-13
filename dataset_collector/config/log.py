import json
import logging
import logging.handlers
import sys
import traceback
from datetime import datetime

from json_logging import util
import tomlkit

from dataset_collector.config import environment


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    job_id = ""

    def __init__(self, job_id: str):
        super().__init__()
        self.job_id = job_id

    def filter(self, record):
        # prefix record.msg instead of adding a new field
        # to be compliant with Kibana
        record.msg = self.job_id + ': ' + record.msg
        return True


def _get_project_meta():
    with open('pyproject.toml', encoding='utf-8') as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)['tool']['poetry']


pkg_meta = _get_project_meta()
service_name = "job-client"
host = environment.get('DOCKER_HOST_NAME')
command = json.dumps(sys.argv)


class CustomJSONLog(logging.Formatter):
    """
    Customized application logger
    """

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {
            'exc_info': exc_info,
            'filename': record.filename,
        }

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(
            traceback.format_exception(*exc_info)
        ) if exc_info else ''

    def format(self, record):
        utcnow = datetime.utcnow()
        base_obj = {
            "written_at": util.iso_time_format(utcnow),
            "written_ts": util.epoch_nano_second(utcnow),
        }
        if record.exc_info or record.exc_text:
            base_obj.update(self.get_exc_fields(record))

        return json.dumps(
            create_microdata_json_log(record, base_obj)
        )


def create_microdata_json_log(record: logging.LogRecord, base_obj: dict):
    return {
        "@timestamp": base_obj['written_at'],
        "command": command,
        "error.stack": base_obj.get('exc_info'),
        "host": host,
        "message": record.getMessage(),
        "level": record.levelno,
        "levelName": record.levelname,
        "loggerName": record.name,
        "schemaVersion": "v3",
        "serviceName": service_name,
        "serviceVersion": str(pkg_meta['version']),
        "thread": record.threadName
    }
