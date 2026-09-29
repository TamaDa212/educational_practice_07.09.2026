import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE_DIR = HERE.parent / "Разработка ядра алгоритма расчета материалов"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
