from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas import NotificationRequest, NotificationResponse
from app.api.dependencies import get_notification_service
from app.core.services import NotificationService
from app.core.models import User, Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post(
    "/send", 
    response_model=NotificationResponse, 
    status_code=status.HTTP_200_OK,
    summary="Envía una notificación mapeando canales y aplicando filtros dinámicos"
)
async def send_notification(
    payload: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    try:
        domain_user = User(**payload.user.model_dump())
        domain_notification = Notification(**payload.notification.model_dump())
        
        results = service.notify(user=domain_user, notification=domain_notification)
        
        return NotificationResponse(
            notification_id=domain_notification.id,
            recipient=domain_user.username,
            status_per_channel=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno procesando la petición: {str(e)}"
        )