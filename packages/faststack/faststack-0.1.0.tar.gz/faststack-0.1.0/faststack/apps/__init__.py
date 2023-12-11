from fastapi import FastAPI
from pathlib import Path
from hypercorn.config import Config as HypercornConfig


class Application:
    name: str

    app_root: Path

    def __init__(self, app_root: Path):
        if not self.name:
            raise ValueError("Application must have a name")

        self.app_root = app_root

    def get_hypercorn_config(self) -> HypercornConfig:
        return HypercornConfig()

    def get_asgi_app(self):
        asgi = FastAPI()

        return asgi
