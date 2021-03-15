import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()
state = {
    # container for global variables:
    "datameta_url": None,
    "token": None
}

@app.callback()
def main(config:Optional[Path] = typer.Option(None)):
    pass

if __name__ == "__main__":
    app()