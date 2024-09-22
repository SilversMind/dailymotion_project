import logging
from src.constants import LOGGER_NAME
from src.utils import color_str
logger = logging.getLogger(LOGGER_NAME)

def send_mail(to_email: str, activation_code: str):
    """
    Mock function to simulate sending an email via a third-party service.
    Logs the activation code to the console.
    """
    logger.info("Sending activation code %s to %s", color_str(activation_code), to_email)
