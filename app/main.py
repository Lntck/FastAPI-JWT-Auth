from fastapi import FastAPI

from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.core.exception_handlers import register_exception_handlers
from app.routers import auth, users


settings = get_settings()

app = FastAPI(
    title="My Auth API",
    version="1.0.0",
    debug=settings.debug,
)

app.state.limiter = limiter
register_exception_handlers(app)
app.include_router(auth.router)
app.include_router(users.router)