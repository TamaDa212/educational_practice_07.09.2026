from db import open_db
from material_calculator import calculate_material_amount


def run_demo(database_path=None):
    connection = open_db(database_path)
    amount = calculate_material_amount(3, 3, 4, 2, 3, connection)
    assert amount == 37
    assert calculate_material_amount(0, 1, 1, 1, 1, connection) == -1
    assert calculate_material_amount(1, 1, -1, 1.5, 2.5, connection) == -1
    connection.close()
    print("demo ok")
    return 0


if __name__ == "__main__":
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        raise SystemExit(run_demo(Path(folder) / "demo.db"))
