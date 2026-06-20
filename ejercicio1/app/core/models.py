from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Any, Optional

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    timezone: str = Field(default="America/Bogota", description="Zona horaria del usuario (IANA)")
    
    channel_preferences: Dict[str, bool] = Field(default_factory=dict)

    def is_channel_enabled(self, channel_name: str) -> bool:
        return self.channel_preferences.get(channel_name.lower(), True)


class Notification(BaseModel):

    id: str
    title: str
    body: str
    event_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = True 