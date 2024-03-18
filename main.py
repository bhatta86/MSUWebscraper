import httpx
from selectolax.parser import HTMLParser
import time


def get_html(baseurl, page):
    """
    Set header to user agent, can be found by typing my user agent in google
    Get response from URL plus page number, allow redirects for page number to work
    Try and except to handle error if page does not exist
    Parse response from page with HTMLParser
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    resp = httpx.get(baseurl + str(page), headers=headers, follow_redirects=True)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url}. Page limit exceeded")
        return False

    html = HTMLParser(resp.text)
    return html


def extract_text(html, sel):
    """
    Error handling in case an acquired value is none
    In this case we are trying to avoid the None values given by sale prices
    """
    try:
        return html.css_first(sel).text()
    except AttributeError as err:
        return None


def parse_page(html):
    """
    Scrapes the products from the site using the class that olds all the objects li.[class]
    Stores product name, type, price, and savings into a dictionary
    """
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    items = []
    for product in products:
        item = {
            "brand": extract_text(product, ".nL0nEPe34KFncpRNS29I"),
            "type": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
            "price": extract_text(product, "span[data-ui=full-price]"),
            "savings": extract_text(product, "div[data-ui=savings-percent-variant2]")
        }
        yield item


def main():
    """
    Define baseurl, website we want to scrape
    Run procedures based on given page range
    """
    baseurl = "https://www.rei.com/c/tents?page="
    for i in range(1, 100):
        print(f"---PAGE {i}---")
        html = get_html(baseurl, i)
        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)
        time.sleep(1)


if __name__ == "__main__":
    main()
