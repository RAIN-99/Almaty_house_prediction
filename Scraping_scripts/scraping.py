import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import csv
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_html(url):
    r = requests.get(url)
    return r.text

 
def write_csv(data):
    with open('../data/raw_data.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['etaj'],
                         data['square'],
                         data['description'],
                         data['adress']))

def get_phone(url):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get(url) 
    sleep(1) 
    tel = driver.execute_script("return window.digitalData")
    #tel = driver.find_element_by_xpath("//script[@type = 'text/javascript']")# присваиваем переменной tel показанные номера телефонов
    #geo=driver.execute_script("return arguments[0].innerHTML",tel)
    driver.quit() 
    return tel 


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml') 
    divs = soup.find('section', class_='a-list') 
    ads = divs.find_all('div', class_='a-card__inc')

    for ad in ads:
        try:
            div = ad.find('a', class_='a-card__title').text
            kv = div.split(",")[0] 
        except:
            kv = ''
        try:
            div = ad.find('a', class_='a-card__title').text
            square = div.split(",")[1]
        except:
            square  = ''
        try:
            div = ad.find('a', class_='a-card__title').text
            etaj = div.split(",")[2]
        except:
            etaj  = ''            

        try:
            price = ad.find('div', class_='a-card__price').text.strip()
        except:
            price = ''
        try:
            descr = ad.find('div', class_='a-card__text-preview').text.strip()
        except:
            descr = ''
        try:
            div = ad.find('div', class_='a-card__header-left')
            url = "https://krisha.kz" + div.find('a').get('href')

        except:
            url = ''

        tel1 = get_phone(url)
        data = {'title':kv,
                'price':price,
                'etaj':etaj,
                'square':square,
                'description':descr,
                'adress':tel1}
        write_csv(data)
            

def main():
    base_url = 'https://krisha.kz/prodazha/kvartiry/almaty/?page='
    # 
    for i in range(1, 2):
        url_gen = base_url + str(i)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()