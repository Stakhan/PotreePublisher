import yaml
import time
import typer
import subprocess
from pathlib import Path
from datetime import timedelta
from .Publisher import Publisher

root_path = Path(__file__).parent.resolve()

def check_path_callback(path: str):
    plp = Path(path)
    if not plp.resolve().exists():
        raise typer.BadParameter(f"Path '{plp.resolve()}' does not exist...")
    return path

cfg = yaml.full_load(open(root_path / 'potree_server_config.yaml'))

app = typer.Typer()

@app.command()
def main(
    input_path: str = typer.Argument(..., help="Path to the point cloud or a folder of point clouds to process. Any type supported by PotreeConverter is possible.", callback=check_path_callback),
    potree_server_root: str = typer.Option(cfg['root'], help='Root path of the potree server.', callback=check_path_callback),
    point_cloud_folder: str = typer.Option(cfg['point_cloud_folder'], help='Folder where the point cloud will be stored after conversion to Potree Format.'),
    viewer_folder: str = typer.Option(cfg['viewer_folder'], help='Folder where the viewer html page will be stored.')
    ):  
    start_time = time.time()

    input_path = Path(input_path)

    publish = Publisher(
        potree_server_root,
        point_cloud_folder,
        viewer_folder
    )

    if input_path.is_file():
        typer.echo(f"Let's publish the {input_path.name} file!")
        publish.single_file(input_path)
    elif input_path.is_dir():
        typer.echo(f"Let's publish the {input_path.name} folder!")
        publish.folder(input_path)

    typer.echo(f"Result published at: {cfg['server_url']}/{viewer_folder}/{publish.title}.html")

    typer.echo(f"----- Execution time: {timedelta(seconds=time.time()-start_time)}")
