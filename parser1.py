import csv
import requests
from bs4 import BeautifulSoup


def replace_slash(text):
    return text.replace('/', '%2F')


def remove_space(value):
    return value.replace(" ", "")


def remove_suffix(txt):
    if txt.endswith("-N"):
        txt = txt[:-2]
    return txt


def compare_prices(article, price, skidka, raznica, ssl):
    url = remove_space(f"https://umico.az/ru/search/{replace_slash(article)}?from_search=true")
    ssl.append(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('span', class_='MPProductItem-Span')

    counter = 1
    for product in products:
        seller = product.find('span', class_='MPProductItem-Seller')
        description = product.find('span', class_='MPTitle')
        if len(products) == 1:
            if 'Division' in seller.text and article.upper() in description.text.upper():
                try:
                    product_price = float(
                        remove_space(product.find('span', class_='MPPrice-RetailPrice').text.replace(' ₼', '')))
                    skidka.append("Есть")
                except AttributeError:
                    product_price = float(
                        remove_space(product.find('span', class_='MPPrice-OldPrice +').text.replace(' ₼', '')))
                    skidka.append("Нет")
                if product_price == float(price):
                    raznica.append("=")
                    return
                if float(price) < product_price:
                    raznica.append(f'+{(product_price - float(price))}')
                    return
                if float(price) > product_price:
                    raznica.append(f'-{(float(price) - product_price)}')
                    return
            else:
                skidka.append('Данного продукта нет на сайте')
                raznica.append('Данного продукта нет на сайте')
                return
        if counter == len(products) or len(products) == 0:
            skidka.append('Данного продукта нет на сайте')
            raznica.append('Данного продукта нет на сайте')
            counter = 1
            return
        if 'Division' in seller.text and article.upper() not in description.text.upper():
            counter += 1
            continue
        if 'Division' in seller.text and article.upper() in description.text.upper():
            try:
                product_price = float(
                    remove_space(product.find('span', class_='MPPrice-RetailPrice').text.replace(' ₼', '')))
                skidka.append("Есть")
            except AttributeError:
                product_price = float(
                    remove_space(product.find('span', class_='MPPrice-OldPrice +').text.replace(' ₼', '')))
                skidka.append("Нет")
            if product_price == float(price):
                raznica.append("=")
                return
            if float(price) < product_price:
                raznica.append(f'+{(product_price - float(price))}')
                return
            if float(price) > product_price:
                raznica.append(f'-{(float(price) - product_price)}')
                return
        else:
            counter += 1
            continue
    return False


article = []
price = []
stock = []
skidka = []
raznica = []
url = []
with open('/Users/user/Dropbox/Мой Mac (MacBook Air — User)/Downloads/1C_Export_for _Umico.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)
    for row in reader:
        article.append(row[0])
        price.append(row[2])
        stock.append(row[3])

for i in range(0, len(article), 1):
    compare_prices(remove_suffix(article[i]), price[i], skidka, raznica, url)
    print(f'|{article[i]}|', f'|{skidka[i]}|', f'|{raznica[i]}|', f'|{url[i]}|')

csv_file_path = "/Users/user/Dropbox/Мой Mac (MacBook Air — User)/Downloads/1C_Export_for _Umico.csv"

# Открываем существующий файл для чтения и записи
with open(csv_file_path, "r+") as file:
    reader = csv.reader(file, delimiter=',')
    rows = list(reader)

    # Добавляем новые названия столбцов в первую строку
    rows[0].extend(["Скидка", "Разница", "Ссылка"])

    # Записываем данные из массивов в соответствующие столбцы
    for i in range(len(skidka)):
        rows[i+1].extend([skidka[i], raznica[i], url[i]])

    # Перезаписываем файл с обновленными данными
    file.seek(0)  # Переходим в начало файла
    writer = csv.writer(file)
    writer.writerows(rows)
    file.truncate()  # Усекаем файл до текущей позиции записи

