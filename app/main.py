from fastapi import FastAPI

from app.api.health import router as health_router
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(title="AI Business Data Investigator")

app.add_middleware(RequestIDMiddleware)
app.include_router(health_router)