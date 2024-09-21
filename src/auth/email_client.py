import logging
from constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

def send_mail(to_email: str, activation_code: str):
    """
    Mock function to simulate sending an email via a third-party service.
    Logs the activation code to the console.
    """
    logger.info(f"Sending activation code {activation_code} to {to_email}")
