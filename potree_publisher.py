import typer
import subprocess
from pathlib import Path
from Publisher import Publisher

def check_path_callback(path: str):
    plp = Path(path)
    if not plp.resolve().exists():
        raise typer.BadParameter(f"Path '{plp.resolve()}' does not exist...")
    return path


app = typer.Typer()

@app.command()
def main(
    input_point_cloud: str = typer.Argument(..., help="Path to the point cloud to process. Any type supported by PotreeConverter is possible."),
    potree_server_root: str = typer.Option('/var/www/potree', help='Root path of the potree server.', callback=check_path_callback),
    point_cloud_folder: str = typer.Option('pointclouds', help='Folder where the point cloud will be stored after conversion to Potree Format.'),
    viewer_folder: str = typer.Option('results', help='Folder where the viewer html page will be stored.')
    ):  
    
    
    typer.echo(f"Let's publish {input_point_cloud}!")

if __name__ == "__main__":
    app()