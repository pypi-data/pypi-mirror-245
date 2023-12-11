import asyncio

import hypercorn.asyncio
import typer

from faststack.cli.util import Application

dev = typer.Typer()


@dev.command()
def serve(app: Application):
    config = app.get_hypercorn_config()
    asgi_app = app.get_asgi_app()

    asyncio.run(hypercorn.asyncio.serve(asgi_app, config))
