from time import sleep
import re
from public.about_driver import get_driver
from public.fs import init_dir, remove_file


def hand_one_chapter(driver, fs):
    """
    处理一章
    """
    title_dom = driver.find_element_by_id(
        'J_BookCnt').find_element_by_tag_name('h3')
    title = title_dom.get_attribute('innerText')
    title = re.sub('\d+$', '', title, 1)
    fs.write(title + '\n')
    print(title)

    # 刺猬猫的比较复杂, 每行有个数字需要去掉
    txt_dom = driver.find_element_by_id(
        'J_BookRead').find_elements_by_class_name('chapter')
    for dom in txt_dom:
        txt = dom.get_attribute('textContent')
        will_del = dom.find_element_by_tag_name('i').text
        txt = re.sub(will_del + '$', '', txt, 1)
        fs.write(txt + '\n')

    links = driver.find_elements_by_tag_name('a')
    for lk in links:
        if lk.text == '下一章':
            href = lk.get_attribute('href')
            driver.get(href)
            return


def link_try(driver, fs):
    """
    链式处理
    """
    # 收费的图片显示, 以此判断
    fis = driver.find_elements_by_id('realBookImage')
    if len(fis) == 0:
        sleep(1.5)
        hand_one_chapter(driver, fs)
        link_try(driver, fs)
    else:
        print('结束')
        return


init_dir()
# 爬取列表, [小说第一章src, 书名]
arr = [
    [' https://www.ciweimao.com/chapter/103464461 ', '龙门无间道']
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
