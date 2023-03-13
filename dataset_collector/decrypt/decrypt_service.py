import logging
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from dataset_collector.config import environment
from dataset_collector.exception import ResourceNotAvailableError, InvalidKeyError

logger = logging.getLogger()

RSA_KEY_DIR = environment.get('RSA_KEY_DIR')
ENCRYPTED_DIR = environment.get('ENCRYPTED_DIR')
DECRYPTED_DIR = environment.get('DECRYPTED_DIR')


def decrypt():
    rsa_key_dir = Path(RSA_KEY_DIR)
    if not rsa_key_dir.exists():
        raise ResourceNotAvailableError('Need to specify a directory containing the rsa keys.')

    encrypted_dir = Path(ENCRYPTED_DIR)
    if not encrypted_dir.exists():
        raise ResourceNotAvailableError('Need to specify a directory containing the encrypted files.')

    decrypted_dir = Path(DECRYPTED_DIR)
    if not os.path.exists(decrypted_dir):
        os.makedirs(decrypted_dir)

    csv_files = [file for file in os.listdir(encrypted_dir) if file.endswith('.csv.encr')]
    if len(csv_files) == 0:
        logger.info(f'No csv.encr files found in {encrypted_dir}. - Nothing to decrypt.')
        exit()

    private_key_location = f'{rsa_key_dir}/microdata_private_key.pem'

    if not Path(private_key_location).is_file():
        raise ResourceNotAvailableError('microdata_private_key.pem not found.')

    # Reads private key from file
    with open(private_key_location, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    for csv_file in csv_files:
        variable_name = csv_file.split(".")[0]

        # decrypt symkey
        encrypted_symkey = f'{encrypted_dir}/{variable_name}.symkey.encr'
        if not encrypted_symkey.is_file():
            raise ResourceNotAvailableError(f'{variable_name}.symkey.encr not found.')

        with open(encrypted_symkey, 'rb') as f:
            symkey = f.read()  # Read the bytes of the encrypted file

        decrypted_symkey = private_key.decrypt(
            symkey,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # decrypt csv file
        with open(f'{encrypted_dir}/{csv_file}', 'rb') as f:
            data = f.read()

        fernet = Fernet(decrypted_symkey)
        try:
            decrypted = fernet.decrypt(data)
            with open(f'{decrypted_dir}/{variable_name}.csv', 'wb') as f:
                f.write(decrypted)
        except InvalidToken as e:
            raise InvalidKeyError(f'Not able to decrypt {variable_name}')

        logger.info(f'Decrypted {csv_file} into {DECRYPTED_DIR}')
