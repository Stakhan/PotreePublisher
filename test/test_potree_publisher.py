import sys
import yaml
import laspy
import pytest
import numpy as np
from pathlib import Path
from common_fixtures import random_las
from typer.testing import CliRunner

root_path = Path(__file__).parent.resolve()

sys.path.insert(0, str(root_path.parent))
from potree_publisher import app

cfg = yaml.full_load(open(root_path.parent / 'potree_server_config.yaml'))

runner = CliRunner()


def test_single_file(random_las):
    result = runner.invoke(app, [str(random_las)])
    assert result.exit_code == 0
    assert str(random_las)+"!" in result.stdout

    