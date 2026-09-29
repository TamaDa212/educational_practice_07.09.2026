import re

from error_log import guard, log_error
from security_audit import audit_sql_sources


def test_sql_queries_are_parameterized():
    findings = audit_sql_sources()
    assert findings == []


def test_exception_is_written_to_log_with_timestamp(tmp_path):
    log_path = tmp_path / "app.log"

    def broken():
        raise ValueError("некорректный размер продукции")

    result = guard(broken, log_path)
    text = log_path.read_text(encoding="utf-8")
    assert result == -1
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)
    assert "некорректный размер продукции" in text
    log_error("проверка записи", log_path)
    assert "проверка записи" in log_path.read_text(encoding="utf-8")
