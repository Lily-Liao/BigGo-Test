import convert
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://shopee.tw/%E7%8E%A9%E5%85%B7-cat.75.2185?brands=5005&locations=-1&page=0&ratingFilter=4'
pre_part_url = 'https://shopee.tw/%E7%8E%A9%E5%85%B7-cat.75.2185?brands=5005&locations=-1&page='
last_part_url = '&ratingFilter=4'

def shopee_info(url):
    soup = convert.parse_html(convert.get_resource(url))
    items = soup.find_all("div", class_ = "col-xs-2-4 shopee-search-item-result__item")

    all_product_title = []
    all_product_price = []

    chinese_dic = convert.word_process()

    for product in items:
        #取得產品標題
        product_title = product.find('div',class_='O6wiAW').string
        #將繁中轉簡中
        product_title = convert.chinese_convert(product_title,chinese_dic)
        all_product_title.append(product_title)
        
        product_price = product.find_all('span',class_='_341bF0')
        if len(product_price)>1:
            product_price_range = [i.text for i in product_price]
            all_product_price.append(product_price_range)
        else:
            product_price_range = [product_price[0].text]
            all_product_price.append(product_price_range)

    return all_product_title,all_product_price


if __name__=='__main__':
    soup = convert.parse_html(convert.get_resource(url))
    total_page = int(soup.find('span',class_='shopee-mini-page-controller__total').text)

    all_info = []
    for i in range(total_page):
        full_url = pre_part_url+str(i)+last_part_url
        print(full_url)
        product_title, product_price = shopee_info(full_url)
        print(len(product_title),len(product_price))
        print('------------------------------------')
        for title, price in zip(product_title, product_price):
            if len(price) > 1:
                price = '${}~${}'.format(price[0],price[1])
            else:
                price = '${}'.format(price[0])

            all_info.append({'title' : title, 'price' : price})
    
    csv_columns=['title','price']
    csv_file = "product_info.csv"
    try:
        with open(csv_file, 'w',encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in all_info:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    
