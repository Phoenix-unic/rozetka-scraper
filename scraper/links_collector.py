import random
import load_django
from rozetka_admin.models import KeyWords, Links
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class LinksCollectorByKeyword():
    """defines a webdriver with builtin setup(can be changed before driver init), 
        allows to perform search by keyword, with certain seller, 
        get pagination and parse data from every link.
        saves data directly to the database"""
    def __init__(self) -> None:
        self.url = 'https://rozetka.com.ua/ua/'
        self.options_args = ["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list", 
                            "--ignore-ssl-errors", '--no-sandbox', '--enable-javascript', '--disable-gpu']
        self.implicitly_wait = 15
        self.window_size = (1600, 900)
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()

    def init_driver(self):
        """inits driver with applying service and options"""
        for arg in self.options_args:
            self.options.add_argument(arg)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.implicitly_wait(self.implicitly_wait)
        self.driver.set_window_size(*self.window_size)

    def search(self, keyword):
        """performs search with given keyword"""
        try:
            search_field = self.driver.find_element(by=By.NAME, value='search')
            search_field.clear()
            search_field.send_keys(keyword)
            search_field.send_keys(Keys.ENTER)
        except Exception as ex:
            print('\n error while performing search \n')
            # print(ex)

    def select_seller(self):
        """selects checkbox with needed seller"""
        try:
            rozetka_seller = self.driver.find_element(by=By.XPATH, value='//a[@data-id="Rozetka"]')
            rozetka_seller.click()
            sleep(random.random())
        except Exception as ex:
            print('\n error while applying seller \n')
            # print(ex)

    @staticmethod
    def save_data(name, link) -> None:
        """saves data to Link model"""
        Links.objects.create(name=name, link=link)

    def collect_items_data(self) -> None:
        """collects items data from current page"""
        items = self.driver.find_elements(by=By.CLASS_NAME, value='goods-tile__heading')
        for item in items:
            try:
                name, link = item.get_attribute('title').split('/')[0], item.get_attribute('href')
                self.save_data(name=name, link=link)
            except Exception as ex:
                print('\n error while collecting name and link \n')
                print(ex)
                continue

    def get_pagination(self) -> int:
        """collects last pagination page if exists, returns none otherwise"""
        try:
            pagination = self.driver.find_elements(by=By.XPATH, value='//a[@class="pagination__link ng-star-inserted"]')[-1].text
            return int(pagination)
        except Exception as ex:
            print('\n no pagination available \n')
            # print(ex)
            return None

    def next_page_click(self) -> None:
        try:
            next_page_button = self.driver.find_element(by=By.XPATH, value='//a[@class="button button--gray button--medium pagination__direction pagination__direction--forward ng-star-inserted"]')
            next_page_button.click()
            sleep(random.randrange(1, 2))
        except Exception as ex:
            print('\n next page is not found \n')
            # print(ex)


def main() -> None:
    keywords = (item for item in KeyWords.objects.filter(status=False))
    scraper = LinksCollectorByKeyword()
    scraper.init_driver()

    with scraper.driver as driver:
        for keyword in keywords:
            driver.get(scraper.url)
            scraper.search(keyword.name)
            scraper.select_seller()
            scraper.collect_items_data()

            pagination = scraper.get_pagination()
            if pagination:
                for _ in range(pagination - 1):
                    scraper.next_page_click()
                    sleep(random.random())
                    scraper.collect_items_data()

            # after completing keyword, change status to 'done'
            print(f'keyword {keyword} is parsed successfully')
            keyword.status = True
            keyword.save()


if __name__ == '__main__':
    main()  # have some fun ))