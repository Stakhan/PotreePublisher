import sys
import yaml
import laspy
import pytest
import shutil
import numpy as np
from pathlib import Path
from common_fixtures import random_las

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from Publisher import Publisher

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))


@pytest.fixture
def publisher_obj():
    return Publisher(
        '/dummy/path/to/file.las',
        cfg['root'],
        cfg['point_cloud_folder'],
        cfg['viewer_folder'])

@pytest.fixture
def folder_random_las(random_las):
    """Generates a folder containing several copies of a random LAS file.

    Args:
        random_las (pytest.fixture): the `common_fixtures.random_las`  fixture

    Returns:
        pathlib.Path: path to the generated folder
    """
    random_folder = random_las.parent / 'random_folder'
    random_folder.mkdir(exist_ok=True)
    for i in range(3):
        shutil.copy(random_las, random_folder / f'random_{i}.las')
        lasfile = laspy.file.File(random_folder / f'random_{i}.las', mode='rw')
        lasfile.X += i*5000
        lasfile.close()
    return random_folder

def test_check_folder(tmp_path, publisher_obj):
   # Creating directory to make sure it exists beforehand 
    root = tmp_path / 'bla'
    folder = 'bla'
    (root / folder).mkdir(parents=True)
    assert (root / folder).exists()
    
    publisher_obj.check_folder(root, folder)

   # should still exist after execution 
    assert (root / folder).exists()

   # Removing directory to make sure it doesn't exists beforehand
    (root / folder).rmdir()
    assert not (root / folder).exists() 

    publisher_obj.check_folder(root, folder)

   # should exist after execution 
    assert (root / folder).exists()

def test_single_file(publisher_obj, random_las):
    
    publisher_obj.single_file(random_las)
    
    pc_location = publisher_obj.potree_server_root / publisher_obj.point_cloud_folder / random_las.stem
    assert (pc_location / "metadata.json").exists()
    assert (pc_location / "octree.bin").exists()
    assert (pc_location / "hierarchy.bin").exists()

def test_folder(publisher_obj, folder_random_las):
    
    publisher_obj.folder(folder_random_las)

    viewer_location = publisher_obj.potree_server_root / publisher_obj.point_cloud_folder / folder_random_las.stem
    viewer_files = [f.stem for f in viewer_location.iterdir()] 
    
    for random_las in folder_random_las.iterdir():
        assert random_las.stem in viewer_files