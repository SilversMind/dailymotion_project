import logging
from src.constants import LOGGER_NAME
from src.utils import color_str
logger = logging.getLogger(LOGGER_NAME)

def send_mail(to_email: str, activation_code: str) -> None:
    """
    Mock send of an activation email to the specified recipient.

    This function logs the activation code and recipient's email address
    instead of sending an actual email. It is intended for testing and 
    demonstration purposes.

    Args:
        to_email (str): The email address of the recipient.
        activation_code (str): The activation code to be sent.
    """
    logger.info("Sending activation code %s to %s", color_str(activation_code), to_email)
