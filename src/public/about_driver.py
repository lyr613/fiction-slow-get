from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep

# chromedriver放置位置
driver_path = './chromedriver'


def get_driver(src):
    '''传入网址, 获取driver
    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path=driver_path, chrome_options=chrome_options)
    driver.get(src)
    sleep(2)
    return driver
