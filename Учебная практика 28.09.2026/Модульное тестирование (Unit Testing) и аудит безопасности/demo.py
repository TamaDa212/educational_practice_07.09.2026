import core_path  # noqa: F401

from error_log import guard, log_error
from material_calculator import calculate_material_amount
from security_audit import audit_sql_sources


def run_demo():
    findings = audit_sql_sources()
    assert findings == []
    amount = calculate_material_amount(3, 3, 4, 2, 3)
    assert amount == 37
    assert calculate_material_amount(99, 1, 1, 1, 1) == -1

    def broken():
        raise RuntimeError("сбой расчета для демонстрации лога")

    assert guard(broken) == -1
    log_error("Демонстрация: исключение перехвачено, расчет не прервал приложение")
    print("demo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
