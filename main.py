import json
import time

import requests
from bs4 import BeautifulSoup
import csv
import datetime

from openpyxl.workbook import Workbook

start_time = time.time()

def pag (url, num):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    books = []
    for page in range(1, num + 1):
        url = "https://www.labirint.ru/genres/2308/?display=table&page={page}"

        response = requests.get(url=url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_ = "products-table__body").find_all("tr")
        books.append(books_items)
    return books

def bookes (url, num):
    books_items = pag(url, num)
    books_data = []
    count = 0
    for bi in books_items:
        book_data = bi[0].find_all("td")
        count +=1
        try:
            book_title = book_data[0].find("a").text.strip()
        except:
            book_title = "Нет названия книги"

        try:
            book_author = book_data[1].text.strip()
        except:
            book_author = "нет автора"

        try:
            book_publishing = book_data[2].find_all("a")
            book_publishing = ":".join([bp.text for bp in book_publishing])
        except:
            book_publishing = "нет издательства"
        try:
            book_new_price = book_data[3].find("div", class_ = "price").find("span").find("span").text.strip().replace(" ", "")
        except:
            book_new_price = "нет новой цены"
        try:
            book_old_price = book_data[3].find("span", class_ = "price-gray").text.strip().replace(" ", "")
        except:
            book_old_price = "Нет старой цены"

        books_data.append(
            {
                "book_title": book_title,
                "book_author": book_author,
                "book_publishing": book_publishing,
                "book_new_price": book_new_price,
                "book_old_price": book_old_price
            }
        )
    return books_data

def jsoned(url, num):
    books_data = bookes(url, num)
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"labirint_{cur_time}.json", "w") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def save_excel(data: list):
    headers = list(data[0].keys())
    file_name = "1.xlsx"

    wb = Workbook()
    page = wb.active
    page.title = 'data'
    page.append(headers)
    for book in data[:-1]:
        row = []
        for k, v in book.item():
            row.append()
        page.append(row)
    wb.save(filename = file_name)



url = "https://www.labirint.ru/genres/2308/?display=table"
num = 5

if __name__ == "__main__":
    finish_time = time.time() - start_time
    jsoned(url, num)
    print(f"Затраченное на работу скрипта время: {finish_time}")