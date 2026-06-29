from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote


BASE_URL = "https://speedhome.com"


def get_html(search=None, url=None):

    print("NEW SCRAPER LOADED")

    if url and url.strip():

        target_url = url.strip()

    elif search and search.strip():

        keyword = search.strip()

        slug = keyword.lower().replace(" ", "-")

        query = keyword.replace(" ", "+")

        target_url = (
            f"{BASE_URL}/rent/{slug}"
            f"?q={query}&category=LOCATION"
        )

    else:

        target_url = BASE_URL

    print(target_url)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1366,
                "height": 768
            }
        )

        page.goto(
            target_url,
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(5000)

        last_height = 0

        for _ in range(25):

            page.mouse.wheel(0, 7000)

            page.wait_for_timeout(1000)

            new_height = page.evaluate(
                "document.body.scrollHeight"
            )

            if new_height == last_height:
                break

            last_height = new_height

        print("Total link:", page.locator("a").count())

        page.screenshot(
            path="speedhome.png",
            full_page=True
        )

        print("Page title:", page.title())

        print("Total link:", page.locator("a").count())

        print("Total headings:", page.locator("h1,h2,h3,h4").count())

        page.screenshot(
            path="speedhome.png",
            full_page=True
        )

        html = page.content()

        browser.close()

    return html

def get_text(element):

    if element:
        return element.get_text(" ", strip=True)

    return ""


def parse_properties(html):

    soup = BeautifulSoup(html, "lxml")

    cards = soup.find_all(
        "a",
        class_=lambda x: x and "PropertyCard_propertyCard" in x
    )

    print("Jumlah Property Card:", len(cards))

    if cards:
        print(cards[0].prettify()[:1000])

    properties = []

    for card in cards:

        href = card.get("href", "")

        if href.startswith("/"):
            href = BASE_URL + href

        # Title
        title = ""

        title_tag = card.find(
            "h3",
            class_=lambda x: x and "PropertyCard_propertyTitle" in x
        )

        if title_tag:
            title = get_text(title_tag)

        # Property Specs
        size = ""
        bedroom = ""
        bathroom = ""
        parking = ""

        specs = card.find(
            "div",
            class_=lambda x: x and "PropertySpecs_propertySpecs" in x
        )

        if specs:

            spans = specs.find_all("span")

            if len(spans) >= 4:
                size = get_text(spans[0])
                bedroom = get_text(spans[1])
                bathroom = get_text(spans[2])
                parking = get_text(spans[3])

        # Price
        price = ""

        price_tag = card.find(
            "div",
            class_=lambda x: x and "PropertyCard_propertyPrice" in x
        )

        if price_tag:
            price = get_text(price_tag)

        # Available Date
        available = ""

        available_tag = card.find(
            "div",
            class_=lambda x: x and "PropertyCard_propertyAvailability" in x
        )

        if available_tag:
            available = get_text(available_tag)

        if title and price:

            properties.append({

                "Title": title,
                "Price": price,
                "Size": size,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Parking": parking,
                "Available": available,
                "Link": href

            })

    df = pd.DataFrame(properties)

    df = df.drop_duplicates()

    return df
