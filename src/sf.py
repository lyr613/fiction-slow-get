from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import re
from public.about_driver import get_driver
from public.fs import init_dir, remove_file


def hand_one_chapter(driver, fs):
    """
    处理一章
    """
    title_dom = driver.find_element_by_class_name('article-title')
    title = title_dom.get_attribute('innerText')
    print(title)

    txt_dom = driver.find_element_by_id('ChapterBody')
    txt = txt_dom.get_attribute('innerText')
    fs.write(title + '\n' + txt + '\n')

    links = driver.find_elements_by_tag_name('a')
    for lk in links:
        if lk.text == '下一章':
            lk.click()
            return


def link_try(driver, fs):
    """
    链式处理
    """
    # vip地址不一样
    curl = driver.current_url
    if re.search('vip', curl) == None:
        sleep(1.5)
        hand_one_chapter(driver, fs)
        link_try(driver, fs)
    else:
        print('结束')
        return


init_dir()
# 爬取列表, [小说第一章src, 书名]
arr = [
    [' http://book.sfacg.com/Novel/169535/268882/2298443/ ', '黑化的少女们与我支离破碎的日常'],
]

for sf in arr:
    try:
        src, name = sf
        file_src = './result/{}.txt'.format(name)
        print('----{}----'.format(name))

        remove_file(file_src)
        driver = get_driver(src)
        fs = open(file_src, 'a', encoding='utf-8')

        link_try(driver, fs)
    finally:
        driver.quit()
        fs.close()
