from db import open_db
from partner_crud import (
    IntegrityError,
    delete_partner,
    get_partner,
    insert_partner,
    list_partners,
    sales_count,
    save_partner,
    update_partner,
)
from partner_edit import PartnerEditWindow, values_from_partner
from screens import render_screen


def test_seed_loads_five_partners(tmp_path):
    connection = open_db(tmp_path / "p.db")
    partners = list_partners(connection)
    assert len(partners) == 5
    loaded = get_partner(4, connection)
    assert loaded["company_name"] == "Новый Контур"
    assert loaded["address"] == "г. Москва, ул. Садовая, 3"
    assert loaded["director"] == "Кузнецова А.Н."
    assert loaded["contact_email"] == "hello@newcontour.ru"
    connection.close()


def test_insert_then_list_shows_new_row(tmp_path):
    connection = open_db(tmp_path / "p.db")
    saved = insert_partner(
        {
            "partner_type": "ЗАО",
            "company_name": "Северная звезда",
            "director": "Иванова И.И.",
            "address": "г. Москва, ул. Мира, 1",
            "email": "star@alliance.ru",
            "phone": "+7 (900) 111-22-33",
            "rating": "3",
        },
        connection,
    )
    names = [item["company_name"] for item in list_partners(connection)]
    assert saved["partner_id"] == 6
    assert "Северная звезда" in names
    html = render_screen("list", {}, partners=list_partners(connection), trail=["Список партнеров"])
    assert "Северная звезда" in html
    assert "Добавить" in html
    connection.close()


def test_update_does_not_break_sales_fk(tmp_path):
    connection = open_db(tmp_path / "p.db")
    before = sales_count(connection, 5)
    updated = update_partner(
        5,
        {
            "partner_type": "ТД",
            "company_name": "ОптМаркет Плюс",
            "director": "Смирнов Д.В.",
            "address": "г. Санкт-Петербург, ул. Оптиков, 10",
            "email": "opt@optmarket.ru",
            "phone": "+7 (812) 300-40-50",
            "rating": "5",
        },
        connection,
    )
    assert updated["company_name"] == "ОптМаркет Плюс"
    assert updated["partner_id"] == 5
    assert sales_count(connection, 5) == before == 1
    connection.close()


def test_update_missing_partner_is_rejected(tmp_path):
    connection = open_db(tmp_path / "p.db")
    try:
        update_partner(
            999,
            {
                "partner_type": "ООО",
                "company_name": "Нет",
                "email": "none@test.ru",
            },
            connection,
        )
        assert False, "expected IntegrityError"
    except IntegrityError as exc:
        assert "не найден" in str(exc)
    connection.close()


def test_cannot_delete_partner_with_sales(tmp_path):
    connection = open_db(tmp_path / "p.db")
    try:
        delete_partner(5, connection)
        assert False, "expected IntegrityError"
    except IntegrityError as exc:
        assert "история продаж" in str(exc)
    assert get_partner(5, connection) is not None
    connection.close()


def test_add_form_is_empty_edit_form_loads_from_db(tmp_path):
    connection = open_db(tmp_path / "p.db")
    add_html = PartnerEditWindow().render_form()
    assert 'name="partner_id" value=""' in add_html
    assert 'name="company_name" value=""' in add_html
    partner = get_partner(4, connection)
    edit_html = PartnerEditWindow(4, values_from_partner(partner)).render_form()
    assert 'name="partner_id" value="4"' in edit_html
    assert "Новый Контур" in edit_html
    assert "Кузнецова А.Н." in edit_html
    assert "ул. Садовая" in edit_html
    assert "hello@newcontour.ru" in edit_html
    connection.close()


def test_save_partner_switches_insert_and_update(tmp_path):
    connection = open_db(tmp_path / "p.db")
    created = save_partner(
        None,
        {
            "partner_type": "ИП",
            "company_name": "Новый",
            "email": "new@test.ru",
            "rating": "1",
        },
        connection,
    )
    changed = save_partner(
        created["partner_id"],
        {
            "partner_type": "ИП",
            "company_name": "Новый изменённый",
            "email": "new@test.ru",
            "rating": "2",
        },
        connection,
    )
    assert created["partner_id"] == changed["partner_id"]
    assert get_partner(created["partner_id"], connection)["company_name"] == "Новый изменённый"
    connection.close()
