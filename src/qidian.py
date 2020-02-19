from selenium import webdriver
from time import sleep
from os import system
from selenium.webdriver.chrome.options import Options

# 随手写的, 不建议使用

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path='./chromedriver', chrome_options=chrome_options)
# 小说目录页
src = 'https://book.qidian.com/info/1004608738#Catalog'


def get_html(src):
    driver.get(src)
    sleep(5)
    box = driver.find_element_by_tag_name('html')
    inn = box.get_attribute('innerHTML')
    fs = open('./list.html', 'w')
    fs.write(inn)
    fs.close()
    # system('node ./src/qidian.js')


def main(src):
    try:
        get_html(src)
    finally:
        driver.quit()


if __name__ == '__main__':
    main(src)
