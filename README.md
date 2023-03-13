# microdata-dataset-collector

#### Collects and decrypts incoming datasets.
Detects encrypted files in ```ENCRYPTED_DIR``` and decrypts them into ```DECRYPTED_DIR```

Two extensions of files are expected:

```.csv.encr``` : Encrypted dataset file.

```.symkey.encr``` : Encrypted file containing the symmetrical key used to decrypt the dataset file.

Both file types get decrypted by using the private RSA key located at ```RSA_KEY_DIR```

#### Triggers dataset import (optionally)
An import pipeline can be triggered by setting the env. variable ```RUN_JOB_SERVICE_CLIENT``` 
to ```True``` (default FALSE), assuming that ```DECRYPTED_DIR``` is configured to point to working directory of the import pipeline. 

The job service client requests job-service for importable datasets and submits POST requests for importing the datasets.

#### How to test

```poetry run pytest --cov=dataset_collector/ -vvv```

#### How to build

```docker build --tag dataset_collector .```

