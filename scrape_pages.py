import requests
import time
import datetime
import scrape_page

def pages_scraper(base_url, page_number):
    all_articles = []
    failed_pages = []
    with requests.Session() as session:
        session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            })
        max_attempts = 3
        retryable_status_codes = {429, 500, 503}
        for page in range (1, page_number + 1):
            for attempt in range(1, max_attempts + 1):
                try:
                    page_url = f"{base_url}?p={page}"
                    articles = scrape_page.page_scraper(page_url, session)
                    for article in articles:
                        article["page"] = page
                        article["scraped_at"] = datetime.datetime.now().isoformat()
                    all_articles.extend(articles)
                    break
                except requests.HTTPError as e:
                    status_code = e.response.status_code
                    if status_code in retryable_status_codes:
                        if attempt == max_attempts:
                            failed_pages.append({"page": page, "error": str(e)})
                        else:
                            time.sleep(2 ** attempt)
                    else:
                        failed_pages.append({"page": page, "error": str(e)})
                except requests.RequestException as e:
                    if attempt == max_attempts:
                        failed_pages.append({"page": page, "error": str(e)})
                    else:
                        time.sleep(2 ** attempt)
    return all_articles, failed_pages