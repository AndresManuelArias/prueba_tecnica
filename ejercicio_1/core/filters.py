from abc import ABC, abstractmethod
from datetime import datetime
import logging


try:
    from zoneinfo import ZoneInfo
except ImportError:
    import pytz

    def ZoneInfo(tz_name: str):
        return pytz.timezone(tz_name)

from ejercicio_1.core.models import User, Notification
from ejercicio_1.core.channels import NotificationChannel

logger = logging.getLogger(__name__)


class NotificationFilter(ABC):

    @abstractmethod
    def allows(self, channel: NotificationChannel, notification: Notification, user: User) -> bool:
        pass


class UserPreferencesFilter(NotificationFilter):


    def allows(self, channel: NotificationChannel, notification: Notification, user: User) -> bool:
        if not user.is_channel_enabled(channel.name):
            logger.warning(
                f" Filtro Aplicado [Preferencias]: El usuario '{user.username}' "
                f"tiene el canal '{channel.name}' deshabilitado."
            )
            return False
        return True


class QuietHoursFilter(NotificationFilter):

#restringe el envio de notificaciones en horas especificas, por defecto esta desde las 22 hasta las 8 de la mañana.
    def __init__(self, start_hour: int = 22, end_hour: int = 8):

        self.start_hour = start_hour
        self.end_hour = end_hour

    def allows(self, channel: NotificationChannel, notification: Notification, user: User) -> bool:

        if channel.name.lower() == "sms":
            try:
                user_tz = ZoneInfo(user.timezone)
            except Exception:
                logger.error(f"Zona horaria inválida '{user.timezone}' para el usuario {user.username}. Usando UTC.")
                user_tz = ZoneInfo("UTC")

            now_utc = datetime.now(ZoneInfo("UTC"))
            user_local_time = now_utc.astimezone(user_tz)
            current_hour = user_local_time.hour

            if self.start_hour > self.end_hour:
                is_quiet_hour = current_hour >= self.start_hour or current_hour < self.end_hour
            else:
                is_quiet_hour = self.start_hour <= current_hour < self.end_hour

            if is_quiet_hour:
                logger.warning(
                    f"⏰ Filtro Aplicado [Quiet Hours]: Bloqueado envío de SMS a '{user.username}'. "
                    f"Hora local del usuario: {user_local_time.strftime('%H:%M')} ({user.timezone}). "
                    f"Rango de silencio: {self.start_hour}:00 a {self.end_hour}:00."
                )
                return False

        return True