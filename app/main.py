from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.rate_limit import limiter

from app.routers import auth


settings = get_settings()

app = FastAPI(
    title="My Auth API",
    version="1.0.0",
    debug=settings.debug,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore[arg-type]
app.include_router(auth.router)