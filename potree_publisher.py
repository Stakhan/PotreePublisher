import typer
import subprocess
from pathlib import Path

def check_path_callback(path: str):
    plp = Path(path)
    if not plp.resolve().exists():
        raise typer.BadParameter(f"Path '{plp.resolve()}' does not exist...")
    return path

def main(
    input_point_cloud: str = typer.Argument(..., help="Path to the point cloud to process. Any type supported by PotreeConverter is possible."),
    potree_server_root: str = typer.Option('/var/www/potree', help='Root path of the potree server.', callback=check_path_callback),
    point_cloud_folder: str = typer.Option('pointclouds', help='Folder where the point cloud will be stored after conversion to Potree Format.'),
    viewer_folder: str = typer.Option('results', help='Folder where the viewer html page will be stored.')
    ):  
    
    
    typer.echo(f"Let's publish {input_point_cloud}!")

class Publisher:

    def __init__(self, input_point_cloud, potree_server_root, point_cloud_folder, viewer_folder):
        self.check_folder(potree_server_root, point_cloud_folder)
        self.check_folder(potree_server_root, viewer_folder)
        
        self.input_point_cloud = Path(input_point_cloud)
        self.potree_server_root = Path(potree_server_root)
        self.point_cloud_folder = point_cloud_folder
        self.viewer_folder = viewer_folder

    def check_folder(root: str, folder: str):
        plp = Path(root) / folder
        if not plp.resolve().exists():
            typer.echo(f'Creating {plp.resolve()}')
            plp.mkdir(parents=True, exist_ok=True)

    def single_file(self):
        (self.potree_server_root / self.point_cloud_folder / self.input_point_cloud.stem).mkdir()
        process = subprocess.Popen(["/usr/local/bin/PotreeConverter","-i",str(self.input_point_cloud.resolve()),"-o","/var/www/potree/pointclouds/$title --title $title"],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout, stderr

        

    def folder(self):
        pass


if __name__ == "__main__":
    typer.run(main)