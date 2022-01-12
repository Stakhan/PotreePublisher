import laspy
import pytest
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

    return Path(filename)