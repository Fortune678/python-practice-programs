"""
LiteAuth API — Application Entry Point
---------------------------------------
Bootstraps the Litestar application, registers all route handlers,
and runs the startup health check.
"""

import logging
from typing import Any

from litestar import Litestar, get
from litestar.exceptions import InternalServerException

from controllers import AuthController, LogoutController, UserManagementController
from utils import run_health_check

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

@get("/")
async def home() -> dict[str, Any]:
    """Root endpoint — returns a welcome message."""
    return {"message": "Welcome to LiteAuth API"}


# ---------------------------------------------------------------------------
# Startup health check
# ---------------------------------------------------------------------------

try:
    run_health_check()
except Exception as exc:
    logger.warning("Health check encountered an error at startup: %s", exc)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = Litestar(
    route_handlers=[
        home,
        AuthController,
        UserManagementController,
        LogoutController,
    ]
)
