from autoscraper import AutoScraper

def scrape_data(url, wanted_list):
    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return result