from google.cloud import logging
from os import getenv

PROJECT_ID = getenv("PROJECT_ID")

# Instantiates a client
logging_client = logging.Client(project=getenv(PROJECT_ID))
# The name of the log to write to
log_name = "DATA_PIPELINE"
# Selects the log to write to
logger = logging_client.logger(log_name)
