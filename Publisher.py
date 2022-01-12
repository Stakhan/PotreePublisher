import typer
import subprocess
from pathlib import Path

class Publisher:

    def __init__(self, input_point_cloud, potree_server_root, point_cloud_folder, viewer_folder):
        self.check_folder(potree_server_root, point_cloud_folder)
        self.check_folder(potree_server_root, viewer_folder)
        
        self.potree_server_root = Path(potree_server_root)
        self.point_cloud_folder = point_cloud_folder
        self.viewer_folder = viewer_folder

    def check_folder(self, root: str, folder: str):
        plp = Path(root) / folder
        if not plp.resolve().exists():
            typer.echo(f'Creating {plp.resolve()}')
            plp.mkdir(parents=True, exist_ok=True)

    def single_file(self, input_point_cloud):
        input_point_cloud = Path(input_point_cloud)
        self.title = input_point_cloud.stem

        typer.echo("Converting to Potree format...")
        output_location = self.potree_server_root / self.point_cloud_folder / self.title
        output_location.mkdir()
        cmd = [ "/usr/local/bin/PotreeConverter",
                "-i",
                str( input_point_cloud.resolve() ),
                "-o",
                str( output_location ),
                "--title",
                self.title]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.poll() != 0:
            typer.echo(stderr)
            raise typer.Exit(code=1)
        
        
            

        

    def folder(self):
        pass

    def prepare_viewer_single_file(self):
        
        with open('template_single_file.html') as fin, open(self.title+'.html', 'w') as fout:
            for line in fin:
                if 'TILE-NAME-HERE' in line:
                    line = line.replace('TILE-NAME-HERE', self.title)
                fout.write(line)

    def prepare_viewer_folder(self):
        pass