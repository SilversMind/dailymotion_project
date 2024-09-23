import logging
from src.constants import LOGGER_NAME, MAILHOG_HOST, MAILHOG_PORT
from src.utils import color_str
import smtplib
from email.mime.text import MIMEText
from abc import ABC, abstractmethod

logger = logging.getLogger(LOGGER_NAME)


class NotificationSender(ABC):
    @abstractmethod
    def send_activation_code(self, to: str, activation_code: str) -> None:
        pass

class EmailSender(NotificationSender):
    def send_activation_code(self, to_email: str, activation_code: str):
        """
        Mock send of an activation email to the specified recipient.

        This function logs the activation code and recipient's email address
        instead of sending an actual email. It is intended for testing and 
        demonstration purposes.

        Args:
            to_email (str): The email address of the recipient.
            activation_code (str): The activation code to be sent.
        """
        logger.info("Mock sending activation code %s to %s via email", color_str(activation_code), to_email)

        msg = MIMEText(f"Your activation code is: {activation_code}")
        msg['Subject'] = 'Activation Code'
        msg['From'] = "noreply@dailymotion.com"
        msg['To'] = to_email

        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.set_debuglevel(0)
            server.send_message(msg)

class SMSSender(NotificationSender):
    def send_activation_code(self, to_phone: str, activation_code: str):
        """
        Mock send of an SMS to the specified recipient.

        This function logs the SMS message and recipient's phone number
        instead of sending an actual SMS. It is intended for testing and 
        demonstration purposes.
        
        Args:
            to_phone (str): The phone number of the recipient.
            activation_code (str): The SMS message to be sent.
        """
        logger.info("Mock sending activation code to %s with message: %s via SMS", to_phone, activation_code)
