
# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.fireboltt.com/collections/boltt-deal",
#     "https://www.fireboltt.com/collections/luxe-collection",
#     "https://www.fireboltt.com/collections/bluetooth-calling-smartwatch",
#     "https://www.fireboltt.com/collections/circle-connect",
#     "https://www.fireboltt.com/collections/audio",
# ]

# semaphore = asyncio.Semaphore(5)


# # -------- Collection Page --------

# collection_schema = {
#     "name": "FireBolttCollection",
#     "baseSelector": "div.grid__item.grid-product",
#     "fields": [

#         {"name": "name",
#          "selector": "a.product__title",
#          "type": "text"},

#         {"name": "price",
#          "selector": "span.sale-price span.money",
#          "type": "text"},

#         {"name": "original_price",
#          "selector": "span.grid-product__price--original span.money",
#          "type": "text"},

#         {"name": "discount",
#          "selector": "span.saving-label",
#          "type": "text"},

#         {"name": "product_url",
#          "selector": "a.grid-product__link",
#          "type": "attribute",
#          "attribute": "href"},

#         {"name": "soldout",
#          "selector": "img.crossed-out",
#          "type": "exists"}
#     ]
# }


# # -------- Product Page Image + Description --------

# product_schema = {
#     "name": "FireBolttProductDetails",
#     "baseSelector": "body",
#     "fields": [

#         {
#             "name": "image",
#             "selector": "img.photoswipe__image",
#             "type": "attribute",
#             "attribute": "data-photoswipe-src"
#         },

#         {
#             "name": "description",
#             "selector": "div.product-single__description p, div.ProductMeta__Description p, p[data-start]",
#             "type": "text"
#         }
#     ]
# }


# # -------- Helpers --------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_image(url):

#     if not url:
#         return ""

#     if url.startswith("//"):
#         url = "https:" + url

#     return url


# # -------- Get Product Image + Description --------

# async def fetch_product_details(crawler, url):

#     async with semaphore:

#         run_config = CrawlerRunConfig(
#             extraction_strategy=JsonCssExtractionStrategy(product_schema),
#             cache_mode=CacheMode.BYPASS,
#             wait_for="css:img.photoswipe__image",
#             page_timeout=90000
#         )

#         for attempt in range(2):

#             try:

#                 result = await crawler.arun(url=url, config=run_config)

#                 if not result or not result.extracted_content:
#                     return "", ""

#                 data = json.loads(result.extracted_content)

#                 if not data:
#                     return "", ""

#                 image = fix_image(data[0].get("image"))
#                 description = data[0].get("description")

#                 return image, description

#             except Exception:

#                 print(f"[Retry {attempt+1}] Failed product fetch:", url)

#         return "", ""


# # -------- Process One Product --------

# async def process_product(crawler, item):

#     if item.get("soldout"):
#         return None

#     name = item.get("name")

#     # Skip sports products
#     if name and "sport" in name.lower():
#         return None

#     price = clean_number(item.get("price"))
#     original_price = clean_number(item.get("original_price"))

#     if not price or not original_price:
#         return None

#     link = item.get("product_url")

#     if not link:
#         return None

#     if link.startswith("/"):
#         link = "https://www.fireboltt.com" + link

#     image, description = await fetch_product_details(crawler, link)

#     # Image mandatory
#     if not image:
#         return None

#     # Description fallback
#     if not description:
#         description = name

#     return {
#         "name": name,
#         "price": price,
#         "currency": "₹",
#         "original_price": original_price,
#         "discount": clean_number(item.get("discount")),
#         "ratings": None,
#         "description": description,
#         "image_link": image,
#         "product_link": link,
#         "organization_id": "DealWallet",
#         "store_id": "Fireboltt",
#         "categories_id": "Electronics"
#     }


# # -------- Scrape Collection --------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(
#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),
#         cache_mode=CacheMode.BYPASS,
#         wait_for="css:div.grid__item.grid-product",
#         scan_full_page=True,
#         page_timeout=90000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return []

#     items = json.loads(result.extracted_content)

#     tasks = []

#     for item in items:
#         tasks.append(process_product(crawler, item))

#     results = await asyncio.gather(*tasks)

#     return [r for r in results if r]


# # -------- Main --------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("fireboltt_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("\nTotal products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())





import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


TARGET_URLS = [
    "https://www.fireboltt.com/collections/boltt-deal",
    "https://www.fireboltt.com/collections/luxe-collection",
    "https://www.fireboltt.com/collections/bluetooth-calling-smartwatch",
    "https://www.fireboltt.com/collections/circle-connect",
    "https://www.fireboltt.com/collections/audio",
]

semaphore = asyncio.Semaphore(5)


# -------- Collection Page --------

collection_schema = {
    "name": "FireBolttCollection",
    "baseSelector": "div.grid__item.grid-product",
    "fields": [

        {"name": "name",
         "selector": "a.product__title",
         "type": "text"},

        {"name": "price",
         "selector": "span.sale-price span.money",
         "type": "text"},

        {"name": "original_price",
         "selector": "span.grid-product__price--original span.money",
         "type": "text"},

        {"name": "discount",
         "selector": "span.saving-label",
         "type": "text"},

        {"name": "product_url",
         "selector": "a.grid-product__link",
         "type": "attribute",
         "attribute": "href"},

        {"name": "soldout",
         "selector": "img.crossed-out",
         "type": "exists"}
    ]
}


# -------- Product Page Image + Description --------

product_schema = {
    "name": "FireBolttProductDetails",
    "baseSelector": "body",
    "fields": [

        {
            "name": "image",
            "selector": "img.photoswipe__image",
            "type": "attribute",
            "attribute": "data-photoswipe-src"
        },

        {
            "name": "description",
            "selector": "div.product-single__description p, div.ProductMeta__Description p, p[data-start]",
            "type": "text"
        }
    ]
}


# -------- Helpers --------

def clean_number(text):

    if not text:
        return None

    num = re.sub(r"[^\d]", "", text)

    return int(num) if num else None


def fix_image(url):

    if not url:
        return ""

    if url.startswith("//"):
        url = "https:" + url

    return url


# -------- Get Product Image + Description --------

async def fetch_product_details(crawler, url):

    async with semaphore:

        run_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(product_schema),
            cache_mode=CacheMode.BYPASS,
            wait_for="css:img.photoswipe__image",
            page_timeout=90000
        )

        for attempt in range(2):

            try:

                result = await crawler.arun(url=url, config=run_config)

                if not result or not result.extracted_content:
                    return "", ""

                data = json.loads(result.extracted_content)

                if not data:
                    return "", ""

                image = fix_image(data[0].get("image"))
                description = data[0].get("description")

                return image, description

            except Exception:

                print(f"[Retry {attempt+1}] Failed product fetch:", url)

        return "", ""


# -------- Process One Product --------

async def process_product(crawler, item):

    if item.get("soldout"):
        return None

    name = item.get("name")

    # Skip sports and glasses products
    if name:
        name_lower = name.lower()
        if (
            "sport" in name_lower
            or "glass" in name_lower
            or "glasses" in name_lower
            or "lens" in name_lower
        ):
            return None

    price = clean_number(item.get("price"))
    original_price = clean_number(item.get("original_price"))

    if not price or not original_price:
        return None

    link = item.get("product_url")

    if not link:
        return None

    if link.startswith("/"):
        link = "https://www.fireboltt.com" + link

    image, description = await fetch_product_details(crawler, link)

    # Image mandatory
    if not image:
        return None

    # Description fallback
    if not description:
        description = name

    return {
        "name": name,
        "price": price,
        "currency": "₹",
        "original_price": original_price,
        "discount": clean_number(item.get("discount")),
        "ratings": None,
        "description": description,
        "image_link": image,
        "product_link": link,
        "organization_id": "DealWallet",
        "store_id": "Fire Boltt",
        "categories_id": "Electronics"
    }


# -------- Scrape Collection --------

async def scrape_collection(crawler, url):

    run_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(collection_schema),
        cache_mode=CacheMode.BYPASS,
        wait_for="css:div.grid__item.grid-product",
        scan_full_page=True,
        page_timeout=90000
    )

    result = await crawler.arun(url=url, config=run_config)

    if not result or not result.extracted_content:
        return []

    items = json.loads(result.extracted_content)

    tasks = []

    for item in items:
        tasks.append(process_product(crawler, item))

    results = await asyncio.gather(*tasks)

    return [r for r in results if r]


# -------- Main --------

async def scrape_all():

    browser_conf = BrowserConfig(headless=True)

    all_products = []

    async with AsyncWebCrawler(config=browser_conf) as crawler:

        for url in TARGET_URLS:

            print("Scraping:", url)

            products = await scrape_collection(crawler, url)

            all_products.extend(products)

    with open("fireboltt_products.json", "w", encoding="utf-8") as f:

        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print("\nTotal products:", len(all_products))


if __name__ == "__main__":

    asyncio.run(scrape_all())