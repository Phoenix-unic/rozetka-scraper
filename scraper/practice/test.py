import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

options_args = ["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list", 
                "--ignore-ssl-errors", '--no-sandbox', '--enable-javascript', '--disable-gpu']
for arg in options_args:
    options.add_argument(arg)

driver = webdriver.Chrome(options=options, service=service)
driver.implicitly_wait(10)
driver.set_window_size(1666, 999)

example = 'samsung galaxy'
url = 'https://rozetka.com.ua/ua/'
data_list = []

try:
    driver.get(url)
    actions = ActionChains(driver)

    sleep(5)
    search_field = driver.find_element(by=By.XPATH, value='//input[@name="search"]')
    search_field.clear()
    search_field.send_keys(example)
    sleep(random.random())
    search_field.send_keys(Keys.ENTER)
    sleep(random.random())
    rozetka_seller = driver.find_element(by=By.XPATH, value='//a[@data-id="Rozetka"]')
    rozetka_seller.click()
    sleep(random.random())

    pagination = driver.find_elements(by=By.XPATH, value='//a[@class="pagination__link ng-star-inserted"]')[-1].text
    next_page_button = driver.find_element(by=By.XPATH, value='//a[@class="button button--gray button--medium pagination__direction pagination__direction--forward ng-star-inserted"]')
    for i in range(int(pagination)):
        try:
            actions.move_to_element(next_page_button).perform()
        except Exception :
            pass

        items = driver.find_elements(by=By.XPATH, value='//a[@class="goods-tile__heading ng-star-inserted"]')
        for item in items:
            try:
                name, link = item.text.split('/')[0], item.get_attribute('href')
                data_list.append({'name': name, 'link': link})
            except Exception as ex:
                print(ex)
                continue
        sleep(random.random())
        try:
            next_page_button.click()
        except Exception:
            pass
    print(data_list)
except Exception as ex:
    print(ex)
finally:
    sleep(10)
    driver.close()
    driver.quit()







