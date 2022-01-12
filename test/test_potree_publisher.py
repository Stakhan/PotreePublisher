import sys
import yaml
import laspy
import pytest
import numpy as np
from pathlib import Path
from typer.testing import CliRunner

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from potree_publisher import app

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))

runner = CliRunner()

@pytest.fixture
def random_las():
    """Generate random LAS file.

    Returns:
        pathlib.Path: path to generated LAS file 
    """
    filename = root_path / "test_data" / "random.las"
    (root_path / "test_data").mkdir(exist_ok=True)

    header = laspy.header.Header(scale=[0.001, 0.001, 0.001])
    test_las = laspy.file.File(filename, mode="w", header=header)
    test_las.X = np.random.randint(1000, high=50000, size=1000)
    test_las.Y = np.random.randint(1000, high=50000, size=1000)
    test_las.Z = np.random.randint(1000, high=50000, size=1000)
    test_las.classification = np.random.randint(1, high=14, size=1000)
    test_las.close()

    return Path(filename)

def test_single_file(random_las):
    result = runner.invoke(app, [str(random_las)])
    assert result.exit_code == 0
    assert str(random_las)+"!" in result.stdout

    pc_location = Path(cfg["root"]) / cfg["viewer_folder"] / random_las.stem
    assert (pc_location / "metadata.json").exists()
    assert (pc_location / "octree.bin").exists()
    assert (pc_location / "hierarchy.bin").exists()