import rich.traceback
import typer

from src.cluster_widget import ClusterApp
from src.config import Config
from src.slurm_viewer import SlurmViewer

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def view() -> None:
    """ View the nodes """
    config = Config.init()
    SlurmViewer(config).run()


@app.command()
def test() -> None:
    """ View the nodes """
    config = Config.init()
    ClusterApp(config).run()


if __name__ == "__main__":
    rich.traceback.install(width=200)
    app()
