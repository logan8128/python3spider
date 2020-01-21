'''
create by
logan8128
2020-1-21
'''
# 使用selenium完成对狗东商品的爬取
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from selenium.common import exceptions as ex
import time
import pymongo
brower = webdriver.Chrome()
wait=WebDriverWait(brower,10)
keyword = 'ipad'
url = "https://search.jd.com/Search?keyword=" + quote(keyword)
brower.get(url)
def get_page(page):
    print('start get '+str(page)+' page')
    brower.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    try:
        input_page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-skip input'))) #等到加载出来
        button = brower.find_element_by_css_selector('.p-skip a')
        input_page.clear()
        input_page.send_keys(page)
        button.click()
    except ex.StaleElementReferenceException:  #若出现异常重新捕获
        input_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-skip input')))  # 等到加载出来
        button = brower.find_element_by_css_selector('.p-skip a')
        input_page.clear()
        input_page.send_keys(page)
        button.click()
    l=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.gl-item')))  #等待加载
    lis = brower.find_elements_by_css_selector('.gl-item')  # 得到所有的商品标签
    commodities = []
    for li in lis:
        try:
            price=li.find_element_by_css_selector('.p-price i').text
            name=li.find_element_by_css_selector('.p-name em').text
            shop=li.find_element_by_css_selector('.p-shop a').text
            icons=li.find_element_by_css_selector('.p-icons').text
            commodity={
                'name':name,
                'price':price,
                'shop':shop,
                'icons':icons
            }
            commodities.append(commodity)
        except:
            continue
    if(len(commodities)==0):
        get_page(page)
    else:
        save_mongo_db(commodities)

def save_mongo_db(commodities):
    client=pymongo.MongoClient()
    db=client.jd_test
    collection=db.jd_ipad3
    collection.insert_many(commodities)
    print(collection.find().count())

if __name__=='__main__':
    for i in range(58,101):
        get_page(i)
