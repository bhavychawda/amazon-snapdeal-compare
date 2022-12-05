from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
def search(mysearch):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    print("----- page webscarpping started------")
    
    mysearch=mysearch.replace(' ','+')
    browser.get("https://www.amazon.in/s?k="+mysearch)
    soup=BeautifulSoup(browser.page_source,'html.parser')
    results=soup.find_all('div',{'data-component-type':'s-search-result'})

    search_results=[]
    for item in results:
        atag=item.h2.a
        try:
            get_price=item.find('span','a-price')
            price=get_price.find('span','a-offscreen').text
            title=atag.text.strip()
            
            rating=item.i.text

            link="https://amazon.in"+ atag.get('href')
            if atag.get('href').startswith("/sspa/click?"):
                continue
            get_price=item.find('span','a-price')
            price=get_price.find('span','a-offscreen').text
            image=item.find('img','s-image')
            image=image['src']
            search_results.append({
        'link':link,
        'image':image,
        'price':price,
        'title':title,

            })

        except AttributeError:
            print("one deleted")
    print(search_results)        
    return search_results
   