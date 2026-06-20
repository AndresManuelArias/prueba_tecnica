import uvicorn
from fastapi import FastAPI
from app.api.v1.notifications import router as notifications_v1_router

app = FastAPI(
    title="Notification System API",
    description="Microservicio modular de notificaciones",
    version="1.0.0"
)


app.include_router(notifications_v1_router, prefix="/api/v1")

@app.get("/health", tags=["Infrastructure"])
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)