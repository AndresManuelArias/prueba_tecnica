import logging
from typing import List, Dict
from app.core.models import User, Notification
from app.core.channels import NotificationChannel
from app.core.filters import NotificationFilter

logger = logging.getLogger(__name__)


class NotificationService:


    def __init__(self, channels: List[NotificationChannel], filters: List[NotificationFilter]):

        self.channels = channels
        self.filters = filters

    def notify(self, user: User, notification: Notification) -> Dict[str, str]:

        results = {}
        logger.info(f"🚀 Iniciando proceso de notificación [{notification.id}] para el usuario: '{user.username}'")

        for channel in self.channels:

            is_allowed = True
            for current_filter in self.filters:
                if not current_filter.allows(channel, notification, user):
                    is_allowed = False
                    results[channel.name] = "filtered"
                    break 

            if is_allowed:
                try:

                    channel.send(notification, user)
                    results[channel.name] = "sent"
                    logger.info(f"Notificación enviada con éxito por el canal: '{channel.name}'")
                    
                except Exception as error:
                    error_msg = str(error) or error.__class__.__name__
                    results[channel.name] = f"failed: {error_msg}"
                    
                    logger.error(
                        f"Error crítico en el canal '{channel.name}' al notificar a '{user.username}': {error_msg}",
                        exc_info=True  # Imprime el Traceback completo en los logs de desarrollo
                    )

        return results