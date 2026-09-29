import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRACTICE_ROOT = HERE.parent.parent

UNSAFE_PATTERNS = (
    re.compile(r"""execute\(\s*f["']"""),
    re.compile(r"""execute\(\s*["'][^"']*\{"""),
    re.compile(r"""execute\(\s*[^)\n]*\+"""),
)

SKIP_PARTS = {".venv", "__pycache__", ".pytest_cache"}


def python_files():
    files = []
    for path in PRACTICE_ROOT.rglob("*.py"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        files.append(path)
    return files


def audit_sql_sources():
    findings = []
    for path in python_files():
        text = path.read_text(encoding="utf-8")
        for pattern in UNSAFE_PATTERNS:
            if pattern.search(text):
                findings.append(f"{path}: {pattern.pattern}")
    return findings
