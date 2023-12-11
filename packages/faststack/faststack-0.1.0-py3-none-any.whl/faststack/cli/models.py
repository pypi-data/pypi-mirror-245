import typer

from faststack.apps.finders import ModelFinder
from faststack.cli.util import Application

models = typer.Typer()


@models.command(name="list")
def list_models(app: Application):
    finder = ModelFinder(app.app_root)

    def model_name(m):
        return f"{m.__module__}.{m.__qualname__}"

    for model in sorted(finder.find_models(), key=model_name):
        print(f"- {model_name(model)}")
