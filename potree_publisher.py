import typer
from pathlib import Path

def check_path_callback(path: str):
    plp = Path(path)
    if not plp.resolve().exists():
        raise typer.BadParameter(f"Path '{plp.resolve()}' does not exist...")
    return path

def check_folder(root: str, folder: str):
    plp = Path(root) / folder
    if not plp.resolve().exists():
        typer.echo(f'Creating {plp.resolve()}')
        plp.mkdir(parents=True, exist_ok=True)

def main(
    input_point_cloud: str = typer.Argument(..., help="Path to the point cloud to process. Any type supported by PotreeConverter is possible."),
    potree_server_root: str = typer.Option('/var/www/potree', help='Root path of the potree server.', callback=check_path_callback),
    point_cloud_folder: str = typer.Option('pointclouds', help='Folder where the point cloud will be stored after conversion to Potree Format.'),
    viewer_folder: str = typer.Option('results', help='Folder where the viewer html page will be stored.')
    ):  
    check_folder(potree_server_root, point_cloud_folder)
    check_folder(potree_server_root, viewer_folder)
    
    typer.echo(f"Let's publish {input_point_cloud}!")




if __name__ == "__main__":
    typer.run(main)