from autoscraper import AutoScraper

def scrape_data(url, wanted_list):
    """
    Scrape data from a webpage using AutoScraper.

    Parameters:
    - url (str): The URL of the webpage to scrape.
    - wanted_list (list): A list of strings representing the data elements to extract.

    Returns:
    - result: The scraped data as a dictionary or None if the scraping process fails.

    Example:
    >>> url = 'https://example.com'
    >>> wanted_list = ['Title', 'Description', 'Price']
    >>> scrape_data(url, wanted_list)
    {'Title': 'Product Title', 'Description': 'Product Description', 'Price': '$19.99'}
    """

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return result
