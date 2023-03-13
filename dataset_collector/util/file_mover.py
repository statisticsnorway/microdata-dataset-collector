import os
import shutil
from pathlib import Path

from dataset_collector.config import environment

ENCRYPTED_DIR = environment.get('ENCRYPTED_DIR')
DECRYPTED_DIR = environment.get('DECRYPTED_DIR')

ENCRYPTED_DS_EXTENSION = ".csv.encr"
ENCRYPTED_SYMKEY_EXTENSION = ".symkey.encr"
DECRYPTED_DS_EXTENSION = ".csv"


def move_files(variable_name: str):

    decrypted_dir = Path(DECRYPTED_DIR)
    if not os.path.exists(decrypted_dir):
        os.makedirs(decrypted_dir)

    decrypted_variable_dir = Path(f'{DECRYPTED_DIR}/{variable_name}')
    if not os.path.exists(decrypted_variable_dir):
        os.makedirs(decrypted_variable_dir)

    archive_dir = Path(f'{ENCRYPTED_DIR}/archive')
    exists = os.path.exists(archive_dir)
    if not exists:
        os.makedirs(archive_dir)

    shutil.move(f'{ENCRYPTED_DIR}/{variable_name}.{ENCRYPTED_DS_EXTENSION}',
                f'{archive_dir}/{variable_name}.{ENCRYPTED_DS_EXTENSION}')

    shutil.move(f'{ENCRYPTED_DIR}/{variable_name}.{ENCRYPTED_SYMKEY_EXTENSION}',
                f'{archive_dir}/{variable_name}.{ENCRYPTED_SYMKEY_EXTENSION}')

    shutil.move(f'{ENCRYPTED_DIR}/{variable_name}.json',
                f'{archive_dir}/{variable_name}.json')

    shutil.move(f'{ENCRYPTED_DIR}/{variable_name}.json',
                f'{decrypted_variable_dir}/{variable_name}.json')

    shutil.move(f'{ENCRYPTED_DIR}/{variable_name}.{DECRYPTED_DS_EXTENSION}',
                f'{decrypted_variable_dir}/{variable_name}.{DECRYPTED_DS_EXTENSION}')
