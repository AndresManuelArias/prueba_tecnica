import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import random
from abc import ABC, abstractmethod

from app.core.models import User, Notification


logger = logging.getLogger(__name__)


class NotificationChannel(ABC):

    @property
    @abstractmethod
    def name(self) -> str:

        pass

    @abstractmethod
    def send(self, notification: Notification, user: User) -> bool:

        pass


class EmailChannel(NotificationChannel):


    @property
    def name(self) -> str:
        return "email"

    def send(self, notification: Notification, user: User) -> bool:
        SMTP_SERVER = "localhost"
        SMTP_PORT = 1025
        sender_email = "no-reply@tuplataforma.com"
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = user.email
        msg["Subject"] = notification.title
        msg.attach(MIMEText(notification.body, "plain"))
        
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.sendmail(sender_email, user.email, msg.as_string())
            
            logger.info(f"EMAIL enviado exitosamente a {user.email} (Capturado por Mailpit)")
            return True
        except Exception as e:
            logger.error(f"Fallo al conectar con el servidor SMTP local: {str(e)}")
            raise ConnectionError(f"Error de infraestructura de Email: {str(e)}")


class SMSChannel(NotificationChannel):


    @property
    def name(self) -> str:
        return "sms"

    def send(self, notification: Notification, user: User) -> bool:

        if random.random() < 0.2:  # fallo simulado del 20% de las veces
            raise ConnectionError("SMS gateway timeout: Proveedor externo no responde.")

        logger.info(
            f"Sending SMS to {user.phone_number} | Message: {notification.body[:30]}..."
        )
        return True