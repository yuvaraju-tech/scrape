# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range"
# ]


# # ---------- SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.salepage_variant__dBFvR",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }
#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- PROCESS PRODUCT ----------

# async def process_product(item):

#     name = item.get("name")

#     price = clean_number(item.get("price"))

#     if not price:
#         return None

#     link = fix_link(item.get("product_url"))

#     image = item.get("image")

#     return {
#         "name": name,
#         "price": price,
#         "currency": "₹",
#         "ratings": item.get("ratings"),
#         "reviews": item.get("reviews"),
#         "description": name,
#         "image_link": image,
#         "product_link": link,
#         "organization_id": "DealWallet",
#         "store_id": "HealthKart",
#         "categories_id": "Health"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="css:div.salepage_variant__dBFvR",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return []

#     items = json.loads(result.extracted_content)

#     tasks = []

#     for item in items:
#         tasks.append(process_product(item))

#     results = await asyncio.gather(*tasks)

#     return [r for r in results if r]


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())



# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range"
# ]


# # ---------- SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.salepage_variant__dBFvR",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price",
#             "type": "text"
#         },

#         {
#             "name": "original_price",
#             "selector": "span.variant-old-price",
#             "type": "text"
#         },

#         {
#             "name": "discount",
#             "selector": "div.variant-offer",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }
#     ]
# }


# # ---------- PRODUCT PAGE SCHEMA ----------

# product_schema = {

#     "name": "HealthkartProduct",

#     "baseSelector": "ul",

#     "fields": [

#         {
#             "name": "description",
#             "selector": "li",
#             "type": "text"
#         }
#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- FETCH DESCRIPTION ----------

# async def fetch_description(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(product_schema),

#         cache_mode=CacheMode.BYPASS,

#         page_timeout=90000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return ""

#     data = json.loads(result.extracted_content)

#     if not data:
#         return ""

#     descriptions = [d.get("description") for d in data if d.get("description")]

#     return " ".join(descriptions)


# # ---------- PROCESS PRODUCT ----------

# async def process_product(crawler, item):

#     name = item.get("name")

#     price = clean_number(item.get("price"))

#     if not price:
#         return None

#     link = fix_link(item.get("product_url"))

#     image = item.get("image")

#     description = await fetch_description(crawler, link)

#     if not description:
#         description = name

#     return {
#         "name": name,
#         "price": price,
#         "currency": "₹",
#         "original_price": clean_number(item.get("original_price")),
#         "discount": clean_number(item.get("discount")),
#         "ratings": item.get("ratings"),
#         "description": description,
#         "image_link": image,
#         "product_link": link,
#         "organization_id": "DealWallet",
#         "store_id": "HealthKart",
#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="css:div.salepage_variant__dBFvR",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
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


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())





# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range",
#     "https://www.healthkart.com/all-brands/vitamins-n-supplements?navKey=CL-4541"
# ]


# # ---------- SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.salepage_variant__dBFvR",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price",
#             "type": "text"
#         },

#         {
#             "name": "original_price",
#             "selector": "span.variant-old-price",
#             "type": "text"
#         },

#         {
#             "name": "discount",
#             "selector": "div.variant-offer",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }
#     ]
# }


# # ---------- PRODUCT PAGE SCHEMA (UPDATED DESCRIPTION SELECTOR) ----------

# product_schema = {

#     "name": "HealthkartProduct",

#     "baseSelector": "div.product_overview_product-information__QlepZ",

#     "fields": [

#         {
#             "name": "description",
#             "selector": "li.product_overview_bullet-points__zSLbg",
#             "type": "text"
#         }
#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- FETCH DESCRIPTION ----------

# async def fetch_description(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(product_schema),

#         cache_mode=CacheMode.BYPASS,

#         page_timeout=90000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return ""

#     data = json.loads(result.extracted_content)

#     if not data:
#         return ""

#     descriptions = [d.get("description") for d in data if d.get("description")]

#     return " ".join(descriptions)


# # ---------- PROCESS PRODUCT ----------

# async def process_product(crawler, item):

#     name = item.get("name")

#     price = clean_number(item.get("price"))
#     original_price = clean_number(item.get("original_price"))

#     # PRICE AND ORIGINAL PRICE MANDATORY
#     if not price or not original_price:
#         return None

#     link = fix_link(item.get("product_url"))

#     image = item.get("image")

#     description = await fetch_description(crawler, link)

#     if not description:
#         description = name

#     return {
#         "name": name,
#         "price": price,
#         "currency": "₹",
#         "original_price": original_price,
#         "discount": clean_number(item.get("discount")),
#         "ratings": item.get("ratings"),
#         "description": description,
#         "image_link": image,
#         "product_link": link,
#         "organization_id": "DealWallet",
#         "store_id": "HealthKart",
#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="css:div.salepage_variant__dBFvR",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
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


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())




# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range",
#     "https://www.healthkart.com/all-brands/vitamins-n-supplements?navKey=CL-4541"
# ]


# # ---------- COLLECTION SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.hk-variants",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price",
#             "type": "text"
#         },

#         {
#             "name": "original_price",
#             "selector": "span.variant-old-price",
#             "type": "text"
#         },

#         {
#             "name": "discount",
#             "selector": "div.variant-offer",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }

#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- PROCESS PRODUCT ----------

# def process_product(item):

#     price = clean_number(item.get("price"))
#     original_price = clean_number(item.get("original_price"))

#     if not price or not original_price:
#         return None

#     return {

#         "name": item.get("name"),

#         "price": price,

#         "currency": "₹",

#         "original_price": original_price,

#         "discount": clean_number(item.get("discount")),

#         "ratings": item.get("ratings"),

#         "reviews": item.get("reviews"),

#         "description": item.get("name"),

#         "image_link": item.get("image"),

#         "product_link": fix_link(item.get("product_url")),

#         "organization_id": "DealWallet",

#         "store_id": "HealthKart",

#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="div.hk-variants",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return []

#     items = json.loads(result.extracted_content)

#     products = []

#     for item in items:

#         p = process_product(item)

#         if p:
#             products.append(p)

#     return products


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())





# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range",
#     "https://www.healthkart.com/all-brands/vitamins-n-supplements?navKey=CL-4541"
# ]


# # ---------- COLLECTION PAGE SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.hk-variants",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price, span[class*='price-value-value']",
#             "type": "text"
#         },

#         {
#             "name": "original_price",
#             "selector": "span.variant-old-price, span[class*='mrp-value']",
#             "type": "text"
#         },

#         {
#             "name": "discount",
#             "selector": "div.variant-offer, span[class*='percentage_off']",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }

#     ]
# }


# # ---------- PRODUCT PAGE SCHEMA ----------

# product_schema = {

#     "name": "HealthkartProduct",

#     "baseSelector": "div.product_overview_product-information__QlepZ",

#     "fields": [

#         {
#             "name": "description",
#             "selector": "li.product_overview_bullet-points__zSLbg",
#             "type": "text"
#         }

#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- FETCH DESCRIPTION ----------

# async def fetch_description(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(product_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="div.product_overview_product-information__QlepZ",

#         page_timeout=90000
#     )

#     try:

#         result = await crawler.arun(url=url, config=run_config)

#         if not result or not result.extracted_content:
#             return ""

#         data = json.loads(result.extracted_content)

#         if not data:
#             return ""

#         descriptions = [d.get("description") for d in data if d.get("description")]

#         return " ".join(descriptions)

#     except Exception:
#         return ""


# # ---------- PROCESS PRODUCT ----------

# async def process_product(crawler, item):

#     price = clean_number(item.get("price"))
#     original_price = clean_number(item.get("original_price"))

#     if not price or not original_price:
#         return None

#     link = fix_link(item.get("product_url"))

#     description = await fetch_description(crawler, link)

#     if not description:
#         description = item.get("name")

#     return {

#         "name": item.get("name"),

#         "price": price,

#         "currency": "₹",

#         "original_price": original_price,

#         "discount": clean_number(item.get("discount")),

#         "ratings": item.get("ratings"),

#         "description": description,

#         "image_link": item.get("image"),

#         "product_link": link,

#         "organization_id": "DealWallet",

#         "store_id": "HealthKart",

#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="div.hk-variants",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
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


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())









# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range",
#     "https://www.healthkart.com/all-brands/vitamins-n-supplements?navKey=CL-4541"
# ]


# # ---------- COLLECTION PAGE SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.hk-variants",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price, span[class*='price-value-value']",
#             "type": "text"
#         },

#         {
#             "name": "original_price",
#             "selector": "span.variant-old-price, span[class*='mrp-value']",
#             "type": "text"
#         },

#         {
#             "name": "discount",
#             "selector": "div.variant-offer, span[class*='percentage_off']",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }

#     ]
# }


# # ---------- PRODUCT PAGE SCHEMA (FIXED) ----------

# product_schema = {

#     "name": "HealthkartProduct",

#     "baseSelector": "div[class*='product_overview_product-information']",

#     "fields": [

#         {
#             "name": "description",
#             "selector": "li",
#             "type": "text"
#         }

#     ]
# }


# # ---------- HELPERS ----------

# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- FETCH DESCRIPTION ----------

# async def fetch_description(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(product_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="body",

#         page_timeout=60000
#     )

#     try:

#         result = await crawler.arun(url=url, config=run_config)

#         if not result or not result.extracted_content:
#             return ""

#         data = json.loads(result.extracted_content)

#         if not data:
#             return ""

#         descriptions = [d.get("description") for d in data if d.get("description")]

#         return " ".join(descriptions)

#     except Exception:

#         return ""


# # ---------- PROCESS PRODUCT ----------

# async def process_product(crawler, item):

#     price = clean_number(item.get("price"))
#     original_price = clean_number(item.get("original_price"))

#     if not price or not original_price:
#         return None

#     link = fix_link(item.get("product_url"))

#     description = await fetch_description(crawler, link)

#     if not description:
#         description = item.get("name")

#     return {

#         "name": item.get("name"),

#         "price": price,

#         "currency": "₹",

#         "original_price": original_price,

#         "discount": clean_number(item.get("discount")),

#         "ratings": item.get("ratings"),

#         "reviews": item.get("reviews"),

#         "description": description,

#         "image_link": item.get("image"),

#         "product_link": link,

#         "organization_id": "DealWallet",

#         "store_id": "HealthKart",

#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="div.hk-variants",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
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


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())





# import asyncio
# import json
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# TARGET_URLS = [
#     "https://www.healthkart.com/sale/daily-wellness-range",
# ]


# # ---------- LISTING PAGE SCHEMA ----------

# collection_schema = {

#     "name": "HealthkartCollection",

#     "baseSelector": "div.hk-variants",

#     "fields": [

#         {
#             "name": "name",
#             "selector": "div.variant-name",
#             "type": "text"
#         },

#         {
#             "name": "price",
#             "selector": "span.variant-price, span[class*='price-value-value']",
#             "type": "text"
#         },

#         {
#             "name": "ratings",
#             "selector": "div.flexing-rating-child",
#             "type": "text"
#         },

#         {
#             "name": "reviews",
#             "selector": "div.flexing-reviews",
#             "type": "text"
#         },

#         {
#             "name": "product_url",
#             "selector": "a.variant-link",
#             "type": "attribute",
#             "attribute": "href"
#         },

#         {
#             "name": "image",
#             "selector": "div.variant-img img",
#             "type": "attribute",
#             "attribute": "src"
#         }

#     ]
# }


# # ---------- PRODUCT PAGE SCHEMA ----------

# product_schema = {

#     "name": "HealthkartProduct",

#     "baseSelector": "body",

#     "fields": [

#         {
#             "name": "mrp",
#             "selector": "span.variantInfo_mrp-value__xLlm7",
#             "type": "text"
#         },

#         {
#             "name": "description",
#             "selector": "div.product_overview_product-information__QlepZ li",
#             "type": "text"
#         }

#     ]
# }




# def clean_number(text):

#     if not text:
#         return None

#     num = re.sub(r"[^\d]", "", text)

#     return int(num) if num else None


# def fix_link(link):

#     if not link:
#         return ""

#     if link.startswith("/"):
#         return "https://www.healthkart.com" + link

#     return link


# # ---------- FETCH PRODUCT PAGE DATA ----------

# async def fetch_product_data(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(product_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="span.variantInfo_mrp-value__xLlm7",

#         page_timeout=90000
#     )

#     try:

#         result = await crawler.arun(url=url, config=run_config)

#         if not result or not result.extracted_content:
#             return None

#         data = json.loads(result.extracted_content)

#         if not data:
#             return None

#         mrp = None
#         descriptions = []

#         for d in data:

#             value = clean_number(d.get("mrp"))

#             if value:
#                 mrp = value

#             if d.get("description"):
#                 descriptions.append(d.get("description"))

#         description = " ".join(descriptions)

#         return {
#             "mrp": mrp,
#             "description": description
#         }

#     except Exception:
#         return None


# # ---------- PROCESS PRODUCT ----------

# async def process_product(crawler, item):

#     price = clean_number(item.get("price"))

#     if not price:
#         return None

#     link = fix_link(item.get("product_url"))

#     product_data = await fetch_product_data(crawler, link)

#     if not product_data:
#         return None

#     mrp = product_data["mrp"]

#     # Skip if MRP missing
#     if not mrp:
#         return None

#     discount = int(((mrp - price) / mrp) * 100)

#     description = product_data["description"] or item.get("name")

#     return {

#         "name": item.get("name"),

#         "price": price,

#         "currency": "₹",

#         "original_price": mrp,

#         "discount": discount,

#         "ratings": item.get("ratings"),

#         "description": description,

#         "image_link": item.get("image"),

#         "product_link": link,

#         "organization_id": "DealWallet",

#         "store_id": "HealthKart",

#         "categories_id": "Medical Pharmacy"
#     }


# # ---------- SCRAPE COLLECTION ----------

# async def scrape_collection(crawler, url):

#     run_config = CrawlerRunConfig(

#         extraction_strategy=JsonCssExtractionStrategy(collection_schema),

#         cache_mode=CacheMode.BYPASS,

#         wait_for="div.hk-variants",

#         scan_full_page=True,

#         delay_before_return_html=5,

#         page_timeout=120000
#     )

#     result = await crawler.arun(url=url, config=run_config)

#     if not result or not result.extracted_content:
#         return []

#     items = json.loads(result.extracted_content)

#     products = []

#     for item in items:

#         product = await process_product(crawler, item)

#         if product:
#             products.append(product)

#     return products


# # ---------- MAIN ----------

# async def scrape_all():

#     browser_conf = BrowserConfig(headless=True)

#     all_products = []

#     async with AsyncWebCrawler(config=browser_conf) as crawler:

#         for url in TARGET_URLS:

#             print("Scraping:", url)

#             products = await scrape_collection(crawler, url)

#             all_products.extend(products)

#     with open("healthkart_products.json", "w", encoding="utf-8") as f:

#         json.dump(all_products, f, indent=2, ensure_ascii=False)

#     print("Total products:", len(all_products))


# if __name__ == "__main__":

#     asyncio.run(scrape_all())








import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


TARGET_URLS = [
    "https://www.healthkart.com/sale/daily-wellness-range",
    "https://www.healthkart.com/best-sellers/whey-proteins?navKey=SCT-snt-pt-wp&cache=1"
]


# ---------- LISTING PAGE SCHEMA ----------

collection_schema = {

    "name": "HealthkartCollection",

    "baseSelector": "div.hk-variants",

    "fields": [

        {
            "name": "name",
            "selector": "div.variant-name",
            "type": "text"
        },

        {
            "name": "price",
            "selector": "span.variant-price, span[class*='price-value-value']",
            "type": "text"
        },

        {
            "name": "ratings",
            "selector": "div.flexing-rating-child",
            "type": "text"
        },

        {
            "name": "reviews",
            "selector": "div.flexing-reviews",
            "type": "text"
        },

        {
            "name": "product_url",
            "selector": "a.variant-link",
            "type": "attribute",
            "attribute": "href"
        },

        {
            "name": "image",
            "selector": "div.variant-img img",
            "type": "attribute",
            "attribute": "src"
        }

    ]
}


# ---------- PRODUCT PAGE SCHEMA ----------

product_schema = {

    "name": "HealthkartProduct",

    "baseSelector": "body",

    "fields": [

        {
            "name": "mrp",
            "selector": "span.variantInfo_mrp-value__xLlm7",
            "type": "text"
        },

        {
            "name": "description",
            "selector": "div.product_overview_product-information__QlepZ li",
            "type": "text"
        }

    ]
}


def clean_number(text):

    if not text:
        return None

    num = re.sub(r"[^\d]", "", text)

    return int(num) if num else None


def fix_link(link):

    if not link:
        return ""

    if link.startswith("/"):
        return "https://www.healthkart.com" + link

    return link


# ---------- FETCH PRODUCT PAGE DATA ----------

async def fetch_product_data(crawler, url):

    run_config = CrawlerRunConfig(

        extraction_strategy=JsonCssExtractionStrategy(product_schema),

        cache_mode=CacheMode.BYPASS,

        wait_for="span.variantInfo_mrp-value__xLlm7",

        page_timeout=90000
    )

    try:

        result = await crawler.arun(url=url, config=run_config)

        if not result or not result.extracted_content:
            return None

        data = json.loads(result.extracted_content)

        if not data:
            return None

        mrp = None
        descriptions = []

        for d in data:

            value = clean_number(d.get("mrp"))

            if value:
                mrp = value

            if d.get("description"):
                descriptions.append(d.get("description"))

        description = " ".join(descriptions)

        return {
            "mrp": mrp,
            "description": description
        }

    except Exception:
        return None


# ---------- PROCESS PRODUCT ----------

async def process_product(crawler, item):

    price = clean_number(item.get("price"))

    if not price:
        return None

    link = fix_link(item.get("product_url"))

    # ⬇️ Skip product if product page takes more than 8.9 seconds
    try:
        product_data = await asyncio.wait_for(
            fetch_product_data(crawler, link),
            timeout=8.9
        )
    except asyncio.TimeoutError:
        return None

    if not product_data:
        return None

    mrp = product_data["mrp"]

    # Skip if MRP missing
    if not mrp:
        return None

    discount = int(((mrp - price) / mrp) * 100)

    description = product_data["description"] or item.get("name")

    return {

        "name": item.get("name"),

        "price": price,

        "currency": "₹",

        "original_price": mrp,

        "discount": discount,

        "ratings": item.get("ratings"),

        "description": description,

        "image_link": item.get("image"),

        "product_link": link,

        "organization_id": "DealWallet",

        "store_id": "HealthKart",

        "categories_id": "Medical Pharmacy"
    }


# ---------- SCRAPE COLLECTION ----------

async def scrape_collection(crawler, url):

    run_config = CrawlerRunConfig(

        extraction_strategy=JsonCssExtractionStrategy(collection_schema),

        cache_mode=CacheMode.BYPASS,

        wait_for="div.hk-variants",

        scan_full_page=True,

        delay_before_return_html=5,

        page_timeout=120000
    )

    result = await crawler.arun(url=url, config=run_config)

    if not result or not result.extracted_content:
        return []

    items = json.loads(result.extracted_content)

    products = []

    for item in items:

        product = await process_product(crawler, item)

        if product:
            products.append(product)

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

    with open("healthkart_products.json", "w", encoding="utf-8") as f:

        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print("Total products:", len(all_products))


if __name__ == "__main__":

    asyncio.run(scrape_all())




