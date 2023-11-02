from google.cloud import logging

# Instantiates a client
logging_client = logging.Client(project="your-project-id")
# The name of the log to write to
log_name = "DATA_PIPELINE"
# Selects the log to write to
logger = logging_client.logger(log_name)
