from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from send_mail import *
import smtplib
def pricealert(url,mail,currentprice):
    current_price=1
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    path='/Users/macpc/Documents/chromedriver'
    browser=webdriver.Chrome(options=chrome_options,executable_path=path)

    browser.get("https://www.amazon.in/Apple-iPhone-13-Mini-256GB/dp/B09G99CW2C/ref=sr_1_1_sspa?crid=3CVFG65N4FI5O&keywords=iphone&qid=1669460814&qu=eyJxc2MiOiI2Ljg1IiwicXNhIjoiNi42MiIsInFzcCI6IjYuODEifQ%3D%3D&sprefix=iphon%2Caps%2C378&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1")
    soup=BeautifulSoup(browser.page_source,'html.parser')

    get_price=soup.find('span',"a-price-whole").text
    get_price=get_price[0:len(get_price)-1].replace(',',"")
    if(int(get_price)>current_price):
        print("hgvhfcghgjb")
        # flaskmail(mail,"price drop alert check at "+url)
                    
    
    