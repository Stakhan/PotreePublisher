import sys
import yaml
import laspy
import pytest
import shutil
import numpy as np
from pathlib import Path
from common_fixtures import random_las, folder_random_las

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from Publisher import Publisher

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))


@pytest.fixture
def publisher_obj():
    return Publisher(
        cfg['root'],
        cfg['point_cloud_folder'],
        cfg['viewer_folder'])



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

   # Teardown 
    shutil.rmtree(pc_location, ignore_errors=True)

def test_single_file_fail(publisher_obj):
    non_existing_las = Path('/made/up/path/to/unknown.las')
    
    with pytest.raises(SystemError) as excinfo:
        publisher_obj.single_file(non_existing_las)
 
    # Teardown 
    shutil.rmtree(Path(cfg['root']) / cfg['point_cloud_folder'] / non_existing_las.stem, ignore_errors=True)


def test_folder(publisher_obj, folder_random_las):
    print(folder_random_las)
    publisher_obj.folder(folder_random_las)

    point_cloud_location = publisher_obj.potree_server_root / publisher_obj.point_cloud_folder / folder_random_las.stem
    point_cloud_subfolders = [subf for subf in point_cloud_location.iterdir() if subf.is_dir()]

    for pc_subf in point_cloud_subfolders:
        assert (pc_subf / "metadata.json").exists()
        assert (pc_subf / "octree.bin").exists()
        assert (pc_subf / "hierarchy.bin").exists()

    # Teardown
    shutil.rmtree(point_cloud_location, ignore_errors=True)

def test_prepare_viewer_folder(publisher_obj, folder_random_las):
    
    publisher_obj.folder(folder_random_las)

    viewer_file = publisher_obj.potree_server_root / publisher_obj.viewer_folder / (folder_random_las.stem+'.html')
    assert viewer_file.exists()

   # Teardown
    shutil.rmtree(viewer_file, ignore_errors=True) 