import pytest

from partner_discount import calculate_partner_discount


@pytest.mark.parametrize(
    ("total_quantity", "expected_discount"),
    [
        (9999, 0),
        (10000, 5),
        (49999, 5),
        (50000, 10),
        (299999, 10),
        (300000, 15),
    ],
)
def test_calculate_partner_discount_boundaries(total_quantity, expected_discount):
    actual_discount = calculate_partner_discount(total_quantity)
    assert actual_discount == expected_discount
