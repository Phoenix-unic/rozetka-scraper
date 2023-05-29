import undetected_chromedriver as uc
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



# check mapping
# url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'  # passed

example = 'samsung galaxy'
url = 'https://rozetka.com.ua/ua/'

options = uc.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--enable-javascript')
options.add_argument('--disable-gpu')



with uc.Chrome(options=options) as driver:
    driver.set_window_size(1666, 999)
    driver.implicitly_wait(10)
    actions = ActionChains(driver)

    data_list = []

    driver.get(url)

    # sleep(1)
    search_field = driver.find_element(by=By.XPATH, value='//input[@name="search"]')
    search_field.clear()
    search_field.send_keys(example)
    # sleep(random.random())
    search_field.send_keys(Keys.ENTER)
    # sleep(random.random())
    rozetka_seller = driver.find_element(by=By.XPATH, value='//a[@data-id="Rozetka"]')
    rozetka_seller.click()
    # sleep(random.random())

    pagination = driver.find_elements(by=By.XPATH, value='//a[@class="pagination__link ng-star-inserted"]')[-1].text
    for i in range(int(pagination)):
        next_page_button = driver.find_element(by=By.XPATH, value='//a[@class="button button--gray button--medium pagination__direction pagination__direction--forward ng-star-inserted"]')
        # actions.move_to_element(next_page_button).perform()
        items = driver.find_elements(by=By.XPATH, value='//a[@class="goods-tile__heading ng-star-inserted"]')
        for item in items:
            try:
                name, link = item.text.split('/')[0], item.get_attribute('href')
                data_list.append({'name': name, 'link': link})
            except Exception as ex:
                print(ex)
                continue
        # sleep(2)
        next_page_button.click()
    print(data_list)






























    # actions = ActionChains(driver)
    # driver.implicitly_wait(10)
    # driver.get(url)
    # # sleep(5)
    # search_field = driver.find_element(by=By.XPATH, value='//input[@name="search"]')
    # search_field.clear()
    # search_field.send_keys(example)
    # sleep(random.random())
    # search_field.send_keys(Keys.ENTER)
    # sleep(random.random())

    # rozetka_seller = driver.find_element(by=By.XPATH, value='//a[@data-id="Rozetka"]')
    # rozetka_seller.click()

    # sleep(5)

    # pagination = driver.find_elements(by=By.XPATH, value='//a[@class="pagination__link ng-star-inserted"]')[-1].text
    # for i in range(int(pagination) - 1):
        
    #     for _ in range(5):
    #         driver.execute_script("window.scrollTo(0, 5000);")
    #         sleep(random.random())

    #     # items = driver.find_elements(by=By.XPATH, value='//a[@class="goods-tile__heading ng-star-inserted"]')
    #     # for item in items:
    #     #     try:
    #     #         name, link = item.text.split('/')[0], item.get_attribute('href')
    #     #         # print(name, link)
    #     #         # sleep(random.random())
    #     #     except Exception as ex:
    #     #         # print(ex)
    #     #         continue

    #     next_page_button = driver.find_element(by=By.XPATH, value='//a[@class="button button--gray button--medium pagination__direction pagination__direction--forward ng-star-inserted"]')
    #     next_page_link = next_page_button.get_attribute('href')
    #     print(next_page_link)
    #     # actions.move_to_element(next_page_button).perform()
    #     sleep(15)
    #     next_page_button.click()
    #     sleep(15)


    # sleep(5)
    # # driver.back()

    



class RozetkaLinksCollector():
    ...

