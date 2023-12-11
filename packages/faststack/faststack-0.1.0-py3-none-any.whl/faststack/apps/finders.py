import sys
import importlib.util
import inspect
import re
from pathlib import Path
from types import ModuleType
from typing import TypeVar

from sqlalchemy.sql.sqltypes import MetaData

from faststack.apps import Application
from faststack.models import Model


def load_module_from_path(path: Path) -> ModuleType:
    # Attempt to recreate the module name from the path (relative to project root)
    name = str(path).replace("/", ".")
    name = re.sub(r"\.py$", "", name)
    name = re.sub(r"\.__init__$", "", name)

    if name in sys.modules:
        return sys.modules[name]

    if not importlib.util.find_spec(name):
        raise ValueError(f"Could not find module {name} in {path}")

    # Load the module
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


T = TypeVar('T')


def extract_subclasses(module: ModuleType, base_class: type[T]) -> set[type[T]]:
    return set(filter(
        lambda cls: issubclass(cls, base_class) and cls != base_class,  # noqa: PyCharm bug PY-32860
        [member[1] for member in inspect.getmembers(module, inspect.isclass)]
    ))


class ApplicationFinder:
    APP_MODULE_NAME = "app"

    def __init__(self, context: Path):
        self.context = context

    def find_applications(self) -> list[Application]:
        """
        Import all modules in the current directory + 1 with a module called .app
        Return a list of subclasses of Application

        """

        apps: list[Application] = []

        # Iterate subdirectories of the project root
        for path in self.context.iterdir():
            if not path.is_dir():
                continue

            # Look in app.pys in each subdirectory
            app_py = path / f"{self.APP_MODULE_NAME}.py"
            if not app_py.exists():
                continue

            # Import the app.py
            app = load_module_from_path(app_py)

            # Get subclasses of Application defined in the module
            app_classes = extract_subclasses(app, Application)

            if len(app_classes) > 1:
                raise ValueError(f"Multiple applications found in {app_py} - this is not yet supported")

            # Instantiate the app
            app_cls = list(app_classes)[0]
            apps.append(app_cls(path))

        if len(apps) > 1:
            raise ValueError(f"Multiple applications found in project {self.context} - this is not yet supported")

        return apps


class ModelFinder:
    """Used to enumerate models for debugging, but also to collect models for Alembic migrations"""

    context: Path

    def __init__(self, context: Path):
        self.context = context

    @staticmethod
    def get_metadata() -> MetaData:
        return Model.metadata

    def find_models(self) -> set[type[Model]]:
        return self._recursively_find_models(self.context)

    @staticmethod
    def _recursively_find_models(root: Path) -> set[type[Model]]:
        models: set[type[Model]] = set()

        for path in root.iterdir():
            if path.is_dir():
                models.update(ModelFinder._recursively_find_models(path))
                continue

            if path.suffix != ".py":
                continue

            # Import the module
            module = load_module_from_path(path)

            # Get subclasses of Model defined in the module
            models.update(extract_subclasses(module, Model))

        return models
