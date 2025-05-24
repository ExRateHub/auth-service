from litestar import get
from interface.http.schemas.system import HealthResponse

@get("health/")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


