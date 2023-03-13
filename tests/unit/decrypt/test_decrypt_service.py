import filecmp
import os
from pathlib import Path

from dataset_collector.decrypt import decrypt_service

DECRYPTED_DIR = os.environ['DECRYPTED_DIR']


def test_decrypt():
    decrypt_service.decrypt()

    expected = Path('tests/resources/VARIABLE_1_expected.csv')
    assert filecmp.cmp(f'{DECRYPTED_DIR}/VARIABLE_1.csv', expected)
