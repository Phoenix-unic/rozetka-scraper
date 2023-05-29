import random
import load_django
from rozetka_admin.models import KeyWords, Links
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class RozetkaLinksCollector():
    """performs a search with the unchecked keyword, 
        collects all links from all pages. 
        If no changes needed, only 'collect_links' function needs to be performed."""
    def __init__(self) -> None:
        self.keywords = (item for item in KeyWords.objects.filter(status=False))
        self.links = Links.objects
        self.url = 'https://rozetka.com.ua/ua/'
        self.options_args = ["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list", 
                            "--ignore-ssl-errors", '--no-sandbox', '--enable-javascript', '--disable-gpu']
        self.implicitly_wait = 15
        self.window_size = (1666, 999)
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()

    def apply_options(self) -> None:
        """helps to edit self.options object before applying"""
        for arg in self.options_args:
            self.options.add_argument(arg)

    def init_driver(self) -> None:
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.implicitly_wait(self.implicitly_wait)
        self.driver.set_window_size(*self.window_size)

    def perform_search_with_keyword(self, keyword) -> None:
        try:
            search_field = self.driver.find_element(by=By.XPATH, value='//input[@name="search"]')
            search_field.clear()
            search_field.send_keys(keyword)
            search_field.send_keys(Keys.ENTER)
        except Exception as ex:
            print('error while performing search', ex)

    def apply_seller(self) -> None:
        try:
            rozetka_seller = self.driver.find_element(by=By.XPATH, value='//a[@data-id="Rozetka"]')
            rozetka_seller.click()
        except Exception as ex:
            print('error while applying seller', ex)

    def save_data(self, name, link) -> None:
        self.links.create(name=name, link=link)

    def page_items_collector(self) -> None:
        items = self.driver.find_elements(by=By.XPATH, value='//a[@class="goods-tile__heading ng-star-inserted"]')
        for item in items:
            try:
                name, link = item.text.split('/')[0], item.get_attribute('href')
                self.save_data(name=name, link=link)
            except Exception as ex:
                print('error while collecting name and link', ex)
                continue

    def next_page_click(self) -> None:
        next_page_button = self.driver.find_element(by=By.XPATH, value='//a[@class="button button--gray button--medium pagination__direction pagination__direction--forward ng-star-inserted"]')
        sleep(random.random())
        next_page_button.click()


    @staticmethod
    def keyword_checked(keyword: KeyWords) -> None:
        keyword.status = True
        keyword.save()

    def collect_links(self) -> None:
        self.apply_options()
        self.init_driver()

        self.driver.get(self.url)

        for keyword in self.keywords:
            print(keyword)
            self.perform_search_with_keyword(keyword.name)
            self.apply_seller()
            
            try:  # block try is here for pages with no pagination, data will be collected from current page with exception handling
                pagination = self.driver.find_elements(by=By.XPATH, value='//a[@class="pagination__link ng-star-inserted"]')[-1].text
                for _ in range(int(pagination)):
                    self.page_items_collector()
                    try:
                        self.next_page_click()
                    except Exception as ex:
                        print(ex)
                        break
            except Exception as ex:
                self.page_items_collector()
                print('error while pagination parsing', ex)

            self.keyword_checked(keyword)
                
                
if __name__ == '__main__': 
    scraper = RozetkaLinksCollector()
    scraper.collect_links()





