from fastapi import FastAPI

from app.core.config import get_settings
from app.api.middlewares.rate_limit import limiter
from app.exceptions.handlers import register_exception_handlers
from app.api.v1.router import router as v1_router
from app.core.constants import API_V1_PREFIX


settings = get_settings()

app = FastAPI(
    title="My Auth API",
    version="1.0.0",
    debug=settings.debug,
)

app.state.limiter = limiter
register_exception_handlers(app)
app.include_router(v1_router, prefix=API_V1_PREFIX)