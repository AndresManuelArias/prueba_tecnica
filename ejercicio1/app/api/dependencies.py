from typing import Generator
from app.core.services import NotificationService
from app.core.channels import EmailChannel, SMSChannel
from app.core.filters import UserPreferencesFilter, QuietHoursFilter

def get_notification_service() -> NotificationService:
    channels = [
        EmailChannel(),
        SMSChannel()
    ]
    
    filters = [
        UserPreferencesFilter(),
        QuietHoursFilter(start_hour=22, end_hour=8)
    ]
    
    return NotificationService(channels=channels, filters=filters)