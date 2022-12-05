from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
import string
import os
def singleproduct(url,title,image,price):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    print("-----single page webscarpping started------")
    
    # browser.get(url)
    search_results=[]

    # title=browser.find_element("xpath","//span[@id='productTitle']").text
    # price=browser.find_element("xpath","//span[@class='a-price-whole']").text


    # soup=BeautifulSoup(browser.page_source,'html.parser')
    # parent_image=soup.find(id="imgTagWrapperId")
    # parent_image=parent_image.find('img')

    # image=parent_image['src']

   
   
    search_results.append({
        'link':url,
        'image':image,
        'price':price,
        'title':title,
       

            })
    # title=title.translate(str.maketrans('', '', string.punctuation))
    # title=title.replace(" ","%20").lower()
    # print("-----snapdeal webscarpping started------")  
    # print(title) 
    browser.get("https://www.snapdeal.com/")
    search = browser.find_element('id','inputValEnter')
    search.clear()
    print(title)
    title=title[:45]
    search.send_keys(title)
    search.send_keys(Keys.ENTER)
    sleep(2)
    try:
        snapdeal_price=browser.find_element("xpath","//span[@class='lfloat product-price']").text 
        snapdeal_url=browser.find_element("xpath","//a[@class='dp-widget-link noUdLine hashAdded']")
        snapdeal_image=browser.find_element("xpath","//img[@class='product-image ']")
        search_results.append({
            'link':snapdeal_url.get_attribute('href'),
            'image':snapdeal_image.get_attribute('src'),
            'price':snapdeal_price,
        })
    except:
        search.clear()
        search.send_keys('electronics')
        search.send_keys(Keys.ENTER)
        sleep(2)
        snapdeal_price=browser.find_element("xpath","//span[@class='lfloat product-price']").text 
        snapdeal_url=browser.find_element("xpath","//a[@class='dp-widget-link noUdLine hashAdded']")
        snapdeal_image=browser.find_element("xpath","//img[@class='product-image ']")
        search_results.append({
            'link':snapdeal_url.get_attribute('href'),
            'image':snapdeal_image.get_attribute('src'),
            'price':snapdeal_price,
        })

    print("-----snapdeal webscarpping ended------")   
    return search_results
