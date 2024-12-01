from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger as LOGGER
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api import router
from app.logger import CustomLogger
from app.services import Services
from app.settings import get_settings


class Application(FastAPI):

    def __init__(self):
        self.settings = get_settings()
        self.logger = CustomLogger.make_logger()
        self.services = Services()

        super().__init__(
            title="HIGHLOAD | Test Service",
            description="Testing optimizations when working with high loads",
            root_path_in_servers=True,
            docs_url="/api",
            redoc_url="/api/docs",
            openapi_url="/api/openapi.json",
            default_response_class=ORJSONResponse,
            version=self.settings.APP_RELEASE,
        )
        self.run_startup_actions()

    def run_startup_actions(self) -> None:
        self.add_middlewares()
        self.include_routers()
        self.add_startup_event_handlers()
        self.add_shutdown_event_handlers()

    def include_routers(self) -> None:
        self.include_router(router)
        LOGGER.debug("[MAIN] Routers added")

    def add_middlewares(self) -> None:
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.add_middleware(
            SessionMiddleware,
            secret_key=self.settings.APP_SECRET_KEY,
            max_age=self.settings.AUTH_ACCESS_TOKEN_EXPIRE,
        )
        LOGGER.debug("[MAIN] Middlewares added")

    def add_startup_event_handlers(self) -> None:
        for service in self.services.get_external_services():
            self.add_event_handler("startup", service.start)
            LOGGER.debug(f"[MAIN] Started: {service}")

    def add_shutdown_event_handlers(self) -> None:
        for service in self.services.get_external_services():
            self.add_event_handler("shutdown", service.stop)


app = Application()
