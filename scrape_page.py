import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def page_scraper(url, session):
    articles = []
   
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  
    except requests.HTTPError:
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    title_lines = soup.find_all("span", class_="titleline")
    if title_lines:
        for title_line in title_lines:
            links = title_line.find("a")
            if links:
                href = links.get("href")
                title_link = links.get_text(strip=True)
                if href:
                    link = urljoin(url, href)
                    title = title_link
                else:
                    link = None
                    title = title_link    
            else:
                link = None
                title = title_line.get_text(strip=True)
            article = {
                "title": title,
                "link": link
            }
            articles.append(article)
    else:
        raise Exception(f"No articles found at the URL: {url}")
    return articles