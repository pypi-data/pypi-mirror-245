from pathlib import Path
from typing import Annotated

import typer

from faststack.apps import Application as FaststackApplication
from faststack.apps.finders import ApplicationFinder


def app_callback() -> FaststackApplication:
    """
    Inject the application into the command context

    Usage:
    @app.command()
    def command(app: Application):
        pass

    Raises ValueErrors if no, or more than one, application is found.

    """

    # Find applications in the project
    finder = ApplicationFinder(Path(__name__).parent)
    applications = finder.find_applications()

    if len(applications) == 0:
        raise ValueError("No applications found")

    if len(applications) > 1:
        raise ValueError("Multiple applications found - this is not yet supported")

    return applications[0]


"""
This is a bit of a hack to get non-typer options into the command context.

It's based on this github comment: https://github.com/tiangolo/typer/issues/80#issuecomment-950349503, but the mentioned
missing click paramtype parser override has been implemented since
(https://typer.tiangolo.com/tutorial/parameter-types/custom-types/).

Essentially this adds a hidden CLI option, that is automatically parsed as None, and calls the app_callback to return
the application instance.

I don't know why I need to pass "--app" as the default value, but click seems to treat the value as part of the
param declaration in click/core.py (search: decls + isidentifier). The actual default value set for the parameter is
provided by default_factory.

"""
Application = Annotated[
    FaststackApplication,
    typer.Option("--app", default_factory=lambda: None, callback=app_callback, hidden=True, parser=lambda _: None),
]
