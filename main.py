import scrape_page
import save_scraper

def main():
    articles = scrape_page.page_scraper("https://news.ycombinator.com/")
    save_scraper.save_json(articles, "articles.json")


if __name__ == "__main__":
    main()