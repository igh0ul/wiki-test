import re
from playwright.sync_api import expect

WIKI_HOME = "https://ru.wikipedia.org/"
SEARCH_TERM = "Земля"


def open_earth_article(page):
    page.goto(WIKI_HOME, wait_until="domcontentloaded")
    search = page.get_by_placeholder("Искать в Википедии")
    search.fill(SEARCH_TERM)
    search.press("Enter")
    first_result = page.locator(".mw-search-result-heading a").first
    first_result.click()
    return page.locator("table.infobox")

def test_oxygen_is_20_95_percent(page):
    """Позитивный тест: в инфобоксе видно '20,95 % — кислород' (RU-формат)."""
    infobox = open_earth_article(page)

    # Точное соответствие может отличаться типом пробела (обычный/неразрывный),
    # поэтому используем регулярное выражение и допускаем произвольные пробелы.
    # Проверяем наличие записи '20,95 % — кислород'.
    pattern = re.compile(r"20,95\s*%\s*—\s*кислород", re.I)
    expect(infobox).to_contain_text(pattern)


def test_oxygen_not_english_dot_format(page):
    """Негативный тест: англоязычный формат числа '20.95 % — кислород' НЕ должен встречаться в RU инфобоксе."""
    infobox = open_earth_article(page)
    bad_pattern = re.compile(r"20\.95\s*%\s*—\s*кислород", re.I)
    # Ожидаем, что такого текста нет
    expect(infobox).not_to_contain_text(bad_pattern)
