from pathlib import Path
from tempfile import TemporaryDirectory

from demo import run_demo


def test_crud_demo():
    with TemporaryDirectory() as folder:
        assert run_demo(Path(folder) / "demo.db") == 0
