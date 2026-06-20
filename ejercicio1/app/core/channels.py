import logging
import random
from abc import ABC, abstractmethod
from app.core.models import User, Notification


logger = logging.getLogger(__name__)


class NotificationChannel(ABC):# creación de clase abstracta


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
        logger.info(
            f" Sending EMAIL to {user.email} | Subject: {notification.title} | Body: {notification.body}"
        )

        return True


class SMSChannel(NotificationChannel):


    @property
    def name(self) -> str:
        return "sms"

    def send(self, notification: Notification, user: User) -> bool:

        if random.random() < 0.2:  # fallo simulado del 20% de las veces
            raise ConnectionError("SMS gateway timeout: Proveedor externo no responde.")

        logger.info(
            f" Sending SMS to {user.phone_number} | Message: {notification.body[:30]}..."
        )
        return True