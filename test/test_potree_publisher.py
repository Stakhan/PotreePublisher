import sys
import yaml
import laspy
import pytest
import numpy as np
from pathlib import Path
from common_fixtures import random_las, folder_random_las
from typer.testing import CliRunner

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from potree_publisher import app

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))

runner = CliRunner()


def test_single_file(random_las):
    result = runner.invoke(app, [str(random_las)])
    assert result.exit_code == 0
    assert "file!" in result.stdout

def test_single_file_fail():
    non_existing_las = Path('/made/up/path/to/unknown.las')
    result = runner.invoke(app, [str(non_existing_las)])
    assert result.exit_code == 2
    assert "Path '"+str(non_existing_las)+"' does not exist..." in result.stdout

def test_folder(folder_random_las):
    result = runner.invoke(app, [str(folder_random_las)])
    assert result.exit_code == 0
    assert "folder!" in result.stdout    