import yaml
import typer
import subprocess
from pathlib import Path
from Publisher import Publisher

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
    input_point_cloud: str = typer.Argument(..., help="Path to the point cloud to process. Any type supported by PotreeConverter is possible."),
    potree_server_root: str = typer.Option(cfg['root'], help='Root path of the potree server.', callback=check_path_callback),
    point_cloud_folder: str = typer.Option(cfg['point_cloud_folder'], help='Folder where the point cloud will be stored after conversion to Potree Format.'),
    viewer_folder: str = typer.Option(cfg['viewer_folder'], help='Folder where the viewer html page will be stored.')
    ):  
    
    input_point_cloud = Path(input_point_cloud)

    typer.echo(f"Let's publish {input_point_cloud}!")

    publish = Publisher(
        potree_server_root,
        point_cloud_folder,
        viewer_folder
    )

    if input_point_cloud.is_file():
        publish.single_file(input_point_cloud)
    else:
        raise NotImplementedError("Folder case coming soon.")


if __name__ == "__main__":
    app()