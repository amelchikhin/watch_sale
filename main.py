import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import pandas as pd

DOMEN = "http://forum.watch.ru/"

def get_data(url):
    headers = Headers(os="mac", headers=True).generate()

    responce = requests.get(url=url, headers=headers)

    if responce.status_code == 200:
        return responce.status_code, responce.text
    else:
        raise responce.status_code

def parser_category(html):
    def parser_row(row):
        _ = row.find_all("a")[1]
        title = _.text
        href = _.get('href')

        tail = href.split("&")[-1]
        head = href.split("?")[0]

        url = f"{DOMEN}/{head}?{tail}"

        return {"title": title, "url": url}


    soup = BeautifulSoup(html, 'lxml')
    # _ = soup.find("tbody", id="threadbits_forum_146")
    rows_list = soup.find("tbody", id="threadbits_forum_146").find_all("tr")

    # row = rows_list[0]
    # object_dict = parser_row(row=row)
    res_list = list()
    for row in rows_list:
        object_dict = parser_row(row=row)
        res_list.append(object_dict)
        print(object_dict)

    return res_list

def main():
    url_list = [
        "http://forum.watch.ru/forumdisplay.php?f=146",
        "http://forum.watch.ru/forumdisplay.php?f=192",
        "http://forum.watch.ru/forumdisplay.php?f=193",
        "http://forum.watch.ru/forumdisplay.php?f=93",
        "http://forum.watch.ru/forumdisplay.php?f=130",
        "http://forum.watch.ru/forumdisplay.php?f=94",
        "http://forum.watch.ru/forumdisplay.php?f=131",
        "http://forum.watch.ru/forumdisplay.php?f=161",
        "http://forum.watch.ru/forumdisplay.php?f=162",
        "http://forum.watch.ru/forumdisplay.php?f=173",
        "http://forum.watch.ru/forumdisplay.php?f=174",
        "http://forum.watch.ru/forumdisplay.php?f=147",
    ]

    html = ""

    url = url_list[0]
    status_code, html = get_data(url=url)


    res_list = list()
    for url in url_list:
        _ = parser_category(html=html)
        res_list += _

    df = pd.DataFrame(res_list)
    print(df.head())

    df.to_csv(f"data/data.csv", sep=";")

if __name__ == '__main__':
    main()