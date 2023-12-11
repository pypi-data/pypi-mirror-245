import typer

from .development import dev
from .models import models

app = typer.Typer(pretty_exceptions_short=False)
app.add_typer(dev, name="dev")
app.add_typer(models, name="models")


@app.command()
def version():
    print("0.1.0")
