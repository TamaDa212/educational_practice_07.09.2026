from page import PAGE_TITLE, render_page
from partners import format_rating, list_partners, split_type_and_name


def test_split_type_and_name():
    assert split_type_and_name('ООО "Логистик-Экспресс"') == ("ООО", "Логистик-Экспресс")
    assert split_type_and_name("ИП Петров А.В.") == ("ИП", "Петров А.В.")


def test_format_rating():
    assert format_rating(None) == "—"
    assert format_rating(10) == "10"
    assert format_rating(4.8) == "4.8"


def test_list_partners_has_discount_and_card_fields():
    partners = list_partners()
    assert len(partners) == 5
    first = partners[0]
    assert first["partner_type"] == "ООО"
    assert first["company_name"] == "Логистик-Экспресс"
    assert first["director"] == "Иванов И.И."
    assert "discount_percent" in first
    opt = [item for item in partners if item["partner_id"] == 5][0]
    assert opt["discount_percent"] == 5


def test_page_title_and_resources():
    html = render_page(list_partners())
    assert PAGE_TITLE in html
    assert 'rel="icon" href="/resources/app_icon.png"' in html
    assert 'src="/resources/company_logo.png"' in html
    assert "Логистик-Экспресс" in html
    assert "Обновить" in html
