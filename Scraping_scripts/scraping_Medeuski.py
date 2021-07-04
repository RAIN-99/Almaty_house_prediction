import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('../data/raw_data_medeuski.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['etaj'],
                         data['square'],
                         data['description']))

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

        data = {'title':kv,
                'price':price,
                'etaj':etaj,
                'square':square,
                'description':descr}
        write_csv(data)
            

def main():
    base_url = 'https://krisha.kz/prodazha/kvartiry/almaty-medeuskij/?page='
    # 
    for i in range(1, 247):
        url_gen = base_url + str(i)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()