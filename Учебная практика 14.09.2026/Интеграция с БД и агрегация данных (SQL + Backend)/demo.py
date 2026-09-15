from db import get_connection, initialize_database
from partner_service import get_partner_with_discount


def main():
    connection = get_connection()
    initialize_database(connection)
    partner_ids = [1, 2, 3, 4, 5]
    for partner_id in partner_ids:
        partner = get_partner_with_discount(connection, partner_id)
        print(partner)
    connection.close()


if __name__ == "__main__":
    main()
