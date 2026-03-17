import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


TARGET_URLS = [
    "https://www.hopscotch.in/search?q=%7B%22searchParams%22:%22YXV0b2NvcnJlY3Q9ZmFsc2UmcXVlcnk9c2hvZXMrZm9yK2tpZHM%3D%22,%22searchBy%22:%22shoes%20for%20kids%22%7D",
    "https://www.hopscotch.in/search?q=%7B%22filterQuery%22:%22keyWord%3Dshirts%22,%22keyWord%22:%22shirts%22,%22searchBy%22:%22shirts%22,%22fromSmartFilter%22:true,%22smartFilterType%22:%22genderSmartFilter%22,%22smartFilterValue%22:%22Girl%27s%22,%22smartFilterSequence%22:%22genderSmartFilter%22%7D"
]


# ---------- LISTING SCHEMA ----------

collection_schema = {
    "name": "HopscotchCollection",
    "baseSelector": "div.product-tile",
    "fields": [
        {"name": "name", "selector": "h3", "type": "text"},
        {
            "name": "product_url",
            "selector": "a.product-card-anchor",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "image",
            "selector": "img.plp-image",
            "type": "attribute",
            "attribute": "src"
        }
    ]
}


# ---------- PRODUCT PAGE SCHEMA ----------

product_schema = {
    "name": "HopscotchProduct",
    "baseSelector": "body",
    "fields": [
        {"name": "price", "selector": "span.css-15sf8uw", "type": "text"},
        {"name": "original_price", "selector": "span.css-t8ayun", "type": "text"},
        {"name": "discount", "selector": "span.css-lbn1or", "type": "text"},
        {"name": "description", "selector": "div.css-1ksb9jm", "type": "text"}
    ]
}


# ---------- HELPERS ----------

def clean_number(text):
    if not text:
        return None
    num = re.sub(r"[^\d]", "", text)
    return int(num) if num else None


def fix_link(link):
    if not link:
        return ""
    match = re.search(r"/product/(\d+)", link)
    if match:
        return f"https://www.hopscotch.in/product/{match.group(1)}"
    return ""


def extract_discount(text):
    if not text:
        return None
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else None


# ---------- FETCH PRODUCT DATA ----------

async def fetch_product_data(crawler, url):

    run_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(product_schema),
        cache_mode=CacheMode.BYPASS,
        wait_for="span.css-15sf8uw",
        delay_before_return_html=1,
        page_timeout=30000
    )

    try:
        result = await crawler.arun(url=url, config=run_config)

        if not result or not result.extracted_content:
            return None

        data = json.loads(result.extracted_content)
        if not data:
            return None

        d = data[0]

        return {
            "price": clean_number(d.get("price")),
            "mrp": clean_number(d.get("original_price")),
            "discount": extract_discount(d.get("discount")),
            "description": d.get("description") or ""
        }

    except Exception:
        return None


# ---------- PROCESS PRODUCT ----------

async def process_product(crawler, item):

    name = item.get("name")
    image = item.get("image")

    # ❌ skip invalid image (base64)
    if not image or image.startswith("data:"):
        return None

    link = fix_link(item.get("product_url"))

    if not link:
        return None

    product_data = await fetch_product_data(crawler, link)

    if not product_data:
        return None

    price = product_data["price"]
    mrp = product_data["mrp"]
    discount = product_data["discount"]
    description = product_data["description"]

    # STRICT UI MATCH
    if not price or not mrp or not discount or mrp <= price:
        return None

    return {
        "name": name,
        "price": price,
        "currency": "₹",
        "original_price": mrp,
        "discount": discount,
        "ratings": None,
        "description": description if description else name,
        "image_link": image,
        "product_link": link,
        "organization_id": "DealWallet",
        "store_id": "Hopscotch",
        "categories_id": "Baby & Kids"
    }


# ---------- SCRAPE COLLECTION ----------

async def scrape_collection(crawler, url):

    run_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(collection_schema),
        cache_mode=CacheMode.BYPASS,
        wait_for="div.product-tile",
        scan_full_page=True,
        delay_before_return_html=5,
        page_timeout=120000
    )

    result = await crawler.arun(url=url, config=run_config)

    if not result or not result.extracted_content:
        return []

    items = json.loads(result.extracted_content)

    products = []
    seen_names = set()

    for item in items:

        product = await process_product(crawler, item)

        if not product:
            continue

        # ❌ skip duplicates
        if product["name"] in seen_names:
            continue

        seen_names.add(product["name"])
        products.append(product)

        # 🔢 limit 100
        if len(products) >= 100:
            break

    return products


# ---------- MAIN ----------

async def scrape_all():

    browser_conf = BrowserConfig(headless=True)

    all_products = []

    async with AsyncWebCrawler(config=browser_conf) as crawler:

        for url in TARGET_URLS:
            print("Scraping:", url)

            products = await scrape_collection(crawler, url)
            all_products.extend(products)

    with open("hopscotch_products.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print("Total products:", len(all_products))


if __name__ == "__main__":
    asyncio.run(scrape_all())