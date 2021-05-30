import requests
from bs4 import BeautifulSoup
import time

def short_link(string):
    new_list = list(string)
    count=0
    flag=0

    if 'w' in new_list:
        index1 = new_list.index('w')
        new_list.pop(index1)
        count += 1
    if 'w' in new_list:
        index2 = new_list.index('w')
        if index2 != -1 and index2 == index1:
            new_list.pop(index2)
            count += 1
    if 'w' in new_list:
        index3= new_list.index('w')
        if index3!= -1 and index3== index2 and new_list[index3+1]=='.':
            new_list.pop(index3)
            count+=1
            flag = 1
    if flag == 0:
        start = string.find('/')
        start += 2
        end = string.rfind('.')

        new_string=string[start:end]
        print(new_string)
    elif flag == 1:
        start = string.find('.')
        start = start + 1
        end = string.rfind('.')

        new_string=string[start:end]
        return new_string

def get_smi_links(smi_link):

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }

    answer = requests.get(smi_link, headers=headers)
    soup = BeautifulSoup(answer.text, 'lxml')

    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    with open('links.txt', 'w', encoding='utf8') as f:
        for el in urls:
            f.write(f'{el}\n')

    result = []
    with open('links.txt', 'r', encoding='utf8') as f:
        for line in f:
            result.append(line.strip('\n').strip())

    # print(result.index('/smi/'))
    # print(result.index('//yandex.ru/support/news/info-for-mass-media.xml'))
    # print(result)
    url = result[17]
    mail = result[18]
    cite = short_link(url)
    links = []
    for el in result[19:24]:
        links.append(el)

    # print(url[8:-1])
    # print(mail)
    # print(links)

    with open(f'articles\\{cite}.txt', 'w', encoding='utf8') as f:
        f.write(f'mail: {mail}')
        f.write('\n')
        f.write(f'site: {url}')
        f.write('\n')
        f.write(f'articles:\n')
        for el in links:
            f.write(f'{el}\n')




# sportru = 'https://news.yandex.ru/smi/sportru'
kinopoisk = 'https://news.yandex.ru/smi/kinopoisk'
vedomosti = 'https://news.yandex.ru/smi/vedomosti'
# avtoru = 'https://news.yandex.ru/smi/magautoru'
# geektimes = 'https://news.yandex.ru/smi/geektimes'
# vtimes = 'https://news.yandex.ru/smi/vtimes-io'
# meduza = 'https://news.yandex.ru/smi/meduzaio'
rbc = 'https://news.yandex.ru/smi/rbc'
# thebell = 'https://news.yandex.ru/smi/thebell'
sportru = 'https://news.yandex.ru/smi/sportru'

parsing_url = [vedomosti, rbc, kinopoisk, sportru]

for url in parsing_url:
    get_smi_links(url)
    time.sleep(120)


# def collect_user_smi:
#