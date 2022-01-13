import typer
import subprocess
from pathlib import Path

class Publisher:

    def __init__(self, potree_server_root, point_cloud_folder, viewer_folder):
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

    def launch_PotreeConverter(self, input_path, output_location, title):
        cmd = [ "/usr/local/bin/PotreeConverter",
                "-i",
                str( input_path.resolve() ),
                "-o",
                str( output_location ),
                "--title",
                self.title]
        process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                    )
        stdout, stderr = process.communicate()
        if process.poll() != 0:
            raise SystemError(str(stderr))

    def single_file(self, input_path):
        """Publish a single file

        Args:
            input_path (pathlib.Path): path to file
        """
        self.title = input_path.stem

        typer.echo("Converting to Potree format...")
        output_location = self.potree_server_root / self.point_cloud_folder / self.title
        output_location.mkdir(exist_ok=True)
        
        self.launch_PotreeConverter(input_path, output_location, self.title)
        
        self.prepare_viewer_single_file()
        
    def folder(self, input_path):
        """Publish a whole folder

        Args:
            input_path (pathlib.Path): path to folder
        """
        self.title = input_path.stem
        self.list_tiles =[] 
        output_root = self.potree_server_root / self.point_cloud_folder / self.title
        output_root.mkdir(exist_ok=True)


        file_paths = [fp for fp in input_path.iterdir() if fp.is_file()] 
        lenght = len(file_paths)
        for i,file_path in enumerate(file_paths):
                
                self.list_tiles.append(file_path.stem)
                output_location = output_root / file_path.stem
                if output_location.exists() and all([ (output_location/f).exists() for f in ["metadata.json", "hierarchy.bin", "octree.bin"] ]):
                    typer.echo(f"[{i+1}/{lenght}] File {file_path.name} already prepared. Skipping.")
                    continue
                else:
                    typer.echo(f"[{i+1}/{lenght}] Converting {file_path.name} to Potree format...")
                    output_location.mkdir()
                    self.launch_PotreeConverter(file_path, output_location, file_path.stem)
        
        self.prepare_viewer_folder()

    def prepare_viewer_single_file(self):
        
        with open('viewer_templates/template_single_file.html') as fin, open(self.potree_server_root / self.viewer_folder / (self.title+'.html'), 'w') as fout:
            for line in fin:
                if 'TILE-NAME-HERE' in line:
                    line = line.replace('TILE-NAME-HERE', self.title)
                fout.write(line)

    def prepare_viewer_folder(self):

        with open('viewer_templates/template_folder.html') as fin, open(self.potree_server_root / self.viewer_folder / (self.title+'.html'), 'w') as fout:
            for line in fin:
                if 'LIST-TILE-NAME-HERE' in line:
                    line = line.replace('LIST-TILE-NAME-HERE', str(self.list_tiles))
                if 'TITLE-HERE' in line:
                    line = line.replace('TITLE-HERE', str(self.title))
                fout.write(line)