from pydantic import BaseModel, Field, EmailStr
from typing import Dict, List, Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str = Field(..., examples=["+573001234567"])
    timezone: str = Field(default="America/Bogota", examples=["America/Bogota", "America/Argentina/Buenos_Aires"])
    channel_preferences: Dict[str, bool] = Field(default_factory=dict, examples=[{"email": True, "sms": False, "whatsapp": False}])

class NotificationSchema(BaseModel):
    id: str = Field(..., examples=["notif-999"])
    title: str = Field(..., examples=["Alerta de Seguridad"])
    body: str = Field(..., examples=["Se ha detectado un inicio de sesión inusual en tu cuenta."])
    event_type: str = Field(..., examples=["security"])

class NotificationRequest(BaseModel):
    user: UserSchema
    notification: NotificationSchema

class NotificationResponse(BaseModel):
    notification_id: str
    recipient: str
    status_per_channel: Dict[str, str]
    processed_at: datetime = Field(default_factory=datetime.utcnow)