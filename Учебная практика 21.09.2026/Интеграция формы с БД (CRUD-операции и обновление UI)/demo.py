from db import open_db
from partner_crud import get_partner, list_partners, save_partner
from partner_edit import PartnerEditWindow, values_from_partner
from screens import render_screen


def run_demo(database_path=None):
    connection = open_db(database_path)
    partners = list_partners(connection)
    assert len(partners) == 5
    html = render_screen("list", {}, partners=partners, trail=["Список партнеров"])
    assert "Добавить" in html
    assert "/partner/4/edit" in html

    empty = PartnerEditWindow().render_form()
    assert 'value=""' in empty

    loaded = get_partner(4, connection)
    form = PartnerEditWindow(4, values_from_partner(loaded)).render_form()
    assert "Новый Контур" in form
    assert "ул. Садовая" in form

    save_partner(
        4,
        {
            "partner_type": "ООО",
            "company_name": "Новый Контур",
            "director": "Кузнецова А.Н.",
            "address": "г. Москва, ул. Садовая, 3",
            "email": "hello@newcontour.ru",
            "phone": "+7 (495) 222-33-44",
            "rating": "4",
        },
        connection,
    )
    created = save_partner(
        None,
        {
            "partner_type": "ЗАО",
            "company_name": "Демо Партнёр",
            "director": "Тестов Т.Т.",
            "address": "г. Казань, ул. Баумана, 1",
            "email": "demo@alliance.ru",
            "phone": "+7 (843) 100-20-30",
            "rating": "2",
        },
        connection,
    )
    refreshed = list_partners(connection)
    names = [item["company_name"] for item in refreshed]
    assert "Демо Партнёр" in names
    assert created["partner_id"] == 6
    assert get_partner(4, connection)["company_name"] == "Новый Контур"
    html = render_screen("list", {}, partners=refreshed, trail=["Список партнеров"])
    assert "Демо Партнёр" in html
    connection.close()
    print("demo ok")
    return 0


if __name__ == "__main__":
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        raise SystemExit(run_demo(Path(folder) / "demo.db"))
