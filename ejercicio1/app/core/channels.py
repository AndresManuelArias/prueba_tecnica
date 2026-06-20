import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import random
from abc import ABC, abstractmethod
import urllib.request
import urllib.error
import json
from app.core.config import settings

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
class WhatsAppChannel(NotificationChannel):

    @property
    def name(self) -> str:
        return "whatsapp"

    def send(self, notification: Notification, user: User) -> bool:
        
        if settings.meta_whatsapp_token == "mock_token_dev":
            logger.warning(f"[WhatsApp MOCK] No se detectaron credenciales reales en el .env. Simulando envío a {user.phone_number}")
            return True

        url = f"https://graph.facebook.com/{settings.meta_version_api}/{settings.meta_phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {settings.meta_whatsapp_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": user.phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": f"*{notification.title}*\n\n{notification.body}"
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        try:
            logger.info(f"Enviando WhatsApp API de Meta al número: {user.phone_number}")
            with urllib.request.urlopen(req, timeout=10) as response:
                response_body = response.read().decode("utf-8")
                logger.info(f"WhatsApp enviado con éxito vía Meta. Response: {response_body[:100]}")
                return True
                
        except urllib.error.HTTPError as e:
            error_content = e.read().decode("utf-8")
            logger.error(f"Error devuelto por la API de Meta: Status {e.code} | Response: {error_content}")
            raise ConnectionError(f"Meta API Error ({e.code}): {error_content}")
            
        except Exception as e:
            logger.error(f"Fallo de red o timeout conectando con Meta: {str(e)}")
            raise ConnectionError(f"Fallo de infraestructura en WhatsApp: {str(e)}")