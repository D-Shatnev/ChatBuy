from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.firefox.service import Service as FService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from web_parser import CHROME, FIREFOX, OZON_PRODUCT_CARD_CLASS


class WebParser:
    """ Сontains functions for obtaining links to products from marketplaces."""
    def __init__(self, browser: str =FIREFOX, profile_path: None|str =None) -> None:
        """
        Args:
            browser (str, optional): browser name (firefox or chrome). Defaults to firefox.
            profile_path (None | str, optional): path to firefox profile. Defaults to None.
        """
        self.browser = browser
        self.profile_path = profile_path
        self.driver = None
        self.update_session()

    def update_session(self) -> None:
        """
        Updates session for browser (for making new window for each query).
        It`s necessary to call this method after each query to marketplace.
        """
        self.close_session()
        if self.browser == FIREFOX:
            options = FOptions()
            if self.profile_path:
                options.add_argument(f"-profile {self.profile_path}")
            service = FService(GeckoDriverManager().install())
        else:
            options = COptions()
            service = CService(ChromeDriverManager().install())
        
        self.driver = webdriver.Firefox(service=service, options=options)

    def get_ozon_product_link(self, query: str) -> str|None:
        """
        Searches for the query product in Ozon and returns a link to the most popular product.

        Args:
            query (str): product name that puts to search string.

        Returns:
            str|None: URL to most popular product or None if product is not founded.
        """
        if self.driver is None:
            return None
        self.driver.get(f"https://www.ozon.ru/search/?text={query}&from_global=true")
        #произошла переадресация, url изменился
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)
        query_params["sorting"] = ["rating"]
        encoded_query = urlencode(query_params, doseq=True)
        url_with_rating_sorting = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query,
            parsed_url.fragment
        ))
        self.driver.get(url_with_rating_sorting)
        self.driver.implicitly_wait(2)
        try:
            link = self.driver.find_element(By.CSS_SELECTOR, OZON_PRODUCT_CARD_CLASS)
            return link.get_attribute('href')
        except NoSuchElementException:
            return

    def close_session(self) -> None:
        """Closes current session."""
        if self.driver is not None:
            self.driver.quit()


if __name__ == "__main__":
    parser = WebParser(browser=CHROME)
    #parser = WebParser(browser=FIREFOX, profile_path="/home/kirill/snap/firefox/common/.mozilla/firefox/f2ntg5ly.default")
    print(parser.get_ozon_product_link("Чайник"))   #1 запрос 
    parser.update_session()                         #обновили сессию
    print(parser.get_ozon_product_link("Телескоп")) #2 запрос
    parser.close_session()                          #закрыли сессию