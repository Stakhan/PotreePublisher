import sys
import yaml
import laspy
import pytest
import shutil
import numpy as np
from pathlib import Path
from .common_fixtures import random_las, folder_random_las
from typer.testing import CliRunner

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from PotreePublisher.potreepublisher import app

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))

runner = CliRunner()


def test_command_single_file(random_las):
    result = runner.invoke(app, [str(random_las)])
    assert result.exit_code == 0
    assert "file!" in result.stdout

def test_command_single_file_fail():
    non_existing_las = Path('/made/up/path/to/unknown.las')
    result = runner.invoke(app, [str(non_existing_las)])
    assert result.exit_code == 2
    assert "Path '"+str(non_existing_las)+"' does not exist..." in result.stdout

    # Teardown 
    shutil.rmtree(Path(cfg['root']) / cfg['point_cloud_folder'] /non_existing_las.stem, ignore_errors=True)

def test_command_folder(folder_random_las):
    result = runner.invoke(app, [str(folder_random_las)])
    assert result.exit_code == 0
    assert "folder!" in result.stdout    