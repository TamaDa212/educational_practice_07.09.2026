from db import get_connection, initialize_database
from partner_service import (
    get_partner_with_discount,
    list_partners_with_discount,
    quantity_or_zero,
)


def setup_memory_db():
    connection = get_connection(":memory:")
    initialize_database(connection)
    return connection


def test_partner_with_several_sales():
    connection = setup_memory_db()
    partner = get_partner_with_discount(connection, 1)
    connection.close()
    assert partner["company_name"] == 'ООО "Логистик-Экспресс"'
    assert partner["total_quantity"] == 80
    assert partner["discount_percent"] == 0


def test_partner_without_sales_left_join():
    connection = setup_memory_db()
    partner = get_partner_with_discount(connection, 4)
    connection.close()
    assert partner["company_name"] == 'ООО "Новый Контур"'
    assert partner["total_quantity"] == 0
    assert partner["discount_percent"] == 0


def test_partner_discount_from_aggregated_quantity():
    connection = setup_memory_db()
    partner = get_partner_with_discount(connection, 5)
    connection.close()
    assert partner["total_quantity"] == 10000
    assert partner["discount_percent"] == 5


def test_unknown_partner_returns_none():
    connection = setup_memory_db()
    partner = get_partner_with_discount(connection, 999)
    connection.close()
    assert partner is None


def test_list_partners_with_discount():
    connection = setup_memory_db()
    partners = list_partners_with_discount(connection)
    connection.close()
    assert len(partners) == 5
    by_id = {item["partner_id"]: item for item in partners}
    assert by_id[4]["total_quantity"] == 0
    assert by_id[4]["discount_percent"] == 0
    assert by_id[5]["discount_percent"] == 5
    assert quantity_or_zero(None) == 0
    assert quantity_or_zero("bad") == 0
