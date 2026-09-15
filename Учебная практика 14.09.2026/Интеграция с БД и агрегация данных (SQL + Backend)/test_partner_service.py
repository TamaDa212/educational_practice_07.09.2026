from db import get_connection, initialize_database
from partner_service import get_partner_with_discount


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
