import uvicorn
from typer import Typer

from app.api.main import start_app
from app.core.settings import Config

cli = Typer()
config = Config()


@cli.command()
def run_api() -> None:
    app = start_app()
    uvicorn.run(app, host=config.api.host, port=config.api.port)


if __name__ == "__main__":
    cli()
