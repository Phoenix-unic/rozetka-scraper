import load_django
import random
from rozetka_admin.models import Links, ProductInfo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


class ItemDataCollector():
    """defines webdriver with default options, defines parsing and datasaving methods"""
    def __init__(self) -> None:
        self.item_data = {}
        self.options_args = ["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list", 
                            "--ignore-ssl-errors", '--no-sandbox', '--enable-javascript', '--disable-gpu']
        self.window_size = (1600, 900)
        self.implicitly_wait = 5
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()

    def init_driver(self):
        """inits driver with applying service and options"""
        for arg in self.options_args:
            self.options.add_argument(arg)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.set_window_size(*self.window_size)
        self.driver.implicitly_wait(self.implicitly_wait)
        

    def get_data(self, name: str, link: str) -> None:
        """gets item data from current url"""

        self.item_data['product_name'] = name

        try:
            current_price = self.driver.find_element(by=By.CLASS_NAME, value='product-carriage__price').text.strip()[:-1]
            current_price = int(current_price.replace(' ', ''))
        except (StaleElementReferenceException, ValueError) as ex:
            current_price = 0
            print('an error while collecting price')
            # print(ex)
        self.item_data['current_price'] = current_price
        
        self.item_data['link'] = link

        try:
            reviews = int(self.driver.find_element(by=By.XPATH, value='//a[@class="product__rating-reviews ng-star-inserted"]').text.split()[0])
        except (StaleElementReferenceException, ValueError) as ex:
            reviews = 0
        self.item_data['reviews'] = reviews

        try:
            feature_labels = self.driver.find_elements(by=By.XPATH, value='//dt[@class="characteristics-full__label"]')[:5]
            feature_labels_text = [item.find_element(by=By.TAG_NAME, value='span').text.strip() for item in feature_labels]
        except StaleElementReferenceException :
            feature_labels_text = 'no features label'

        try:
            feature_values = self.driver.find_elements(by=By.XPATH, value='//ul[@class="characteristics-full__sub-list"]')[:5]
            feature_values_text = [item.find_element(by=By.TAG_NAME, value='li').text.strip() for item in feature_values]
        except StaleElementReferenceException :
            feature_values_text = 'no features value'

        self.item_data['features'] = dict(zip(feature_labels_text, feature_values_text))

    def save_data(self):
        """saves product data to corresponding model"""
        ProductInfo.objects.create(
            product_name=self.item_data.get('product_name'),
            current_price=self.item_data.get('current_price'),
            link=self.item_data.get('link'),
            reviews=self.item_data.get('reviews'),
            features=self.item_data.get('features'),
        )


def main() -> None:
    """manages whole scraping process, gets access to the unchecked links in database, 
        performs parsing, saves data, marks link as 'checked' after"""
    links = Links.objects.filter(status=False)
    scraper = ItemDataCollector()
    scraper.init_driver()
    counter = 0

    with scraper.driver as driver:
        for item in links:
            counter += 1
            if counter == 10:
                break
            driver.get(item.link.strip() + 'characteristics/')
            scraper.get_data(name=item.name, link=item.link)
            scraper.save_data()

            # after completing link, change status to 'done'
            item.status = True
            item.save()                


if __name__ == '__main__':
    main()  # have some fun again))



