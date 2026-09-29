from db import open_db
from history_window import PartnerHistoryWindow
from sales_history import get_partner, load_shipments
from screens import render_history, render_list


def run_demo(database_path=None):
    connection = open_db(database_path)
    partner = get_partner(1, connection)
    shipments = load_shipments(1, connection)
    window = PartnerHistoryWindow(partner, shipments)
    html = render_history(window)
    assert "История реализации продукции" in html
    assert "01.03.2026" in html
    assert "Наименование продукции" in html
    list_html = render_list(
        [{"partner_id": 1, "company_name": partner["company_name"], "phone": "—", "rating": "4.8"}],
        1,
    )
    assert "/partner/1/history" in list_html
    connection.close()
    print("demo ok")
    return 0


if __name__ == "__main__":
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        raise SystemExit(run_demo(Path(folder) / "demo.db"))
