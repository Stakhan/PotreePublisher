import laspy
import pytest
import shutil
import numpy as np
from pathlib import Path

root_path = Path(__file__).parent.resolve()


@pytest.fixture
def random_las():
    """Generate random LAS file.

    Returns:
        pathlib.Path: path to generated LAS file 
    """
    filename = root_path / "test_data" / "random.las"
    (root_path / "test_data").mkdir(exist_ok=True)

    test_las = laspy.file.File(filename, mode="w", header=laspy.header.Header())
    allX = np.random.randint(10, high=500, size=1000)
    allY = np.random.randint(10, high=500, size=1000)
    allZ = np.random.randint(10, high=500, size=1000)

    Xmin = np.floor(np.min(allX))
    Ymin = np.floor(np.min(allY))
    Zmin = np.floor(np.min(allZ))

    test_las.header.offset = [Xmin,Ymin,Zmin]
    test_las.header.scale = [0.001,0.001,0.001]

    test_las.X = allX
    test_las.Y = allY
    test_las.Z = allZ
    
    test_las.classification = np.random.randint(1, high=14, size=1000)

    test_las.close()

    yield Path(filename)

    shutil.rmtree(filename, ignore_errors=True)


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
    
    yield random_folder

    shutil.rmtree(random_folder, ignore_errors=True)
