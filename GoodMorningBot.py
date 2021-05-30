import telebot
import requests
from functools import partial
from geopy.geocoders import Nominatim
import datetime
from bs4 import BeautifulSoup
import time
import glob
import json
import random

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows; U; WinNT; en; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable")
token = "1864998452:AAGI9AWWy9kiExZWSM5fqUv8XcnNXiRNR8s"

sportru = 'https://news.yandex.ru/smi/sportru'
kinopoisk = 'https://news.yandex.ru/smi/kinopoisk'
vedomosti = 'https://news.yandex.ru/smi/vedomosti'
avtoru = 'https://news.yandex.ru/smi/magautoru'
geektimes = 'https://news.yandex.ru/smi/geektimes'
vtimes = 'https://news.yandex.ru/smi/vtimes-io'
meduza = 'https://news.yandex.ru/smi/meduzaio'
rbc = 'https://news.yandex.ru/smi/rbc'
thebell = 'https://news.yandex.ru/smi/thebell'

parsing_url = [vedomosti, rbc, kinopoisk, sportru, geektimes, vtimes, meduza, thebell, avtoru]

# f = open("log.txt", "w") #использовалось только для первого запуска, чтобы создать файл.
# f.close()

def what_weather(city):
	"""Определят погоду в требуемом пользователю городе"""
	url = f'http://wttr.in/{city}'
	weather_parameters = {
		'format': 2,
		'M': ''
	}
	try:
		response = requests.get(url, params=weather_parameters)
	except requests.ConnectionError:
		return '<сетевая ошибка>'
	if response.status_code == 200:
		return response.text.strip()
	else:
		return '<ошибка на сервере погоды>'


def currency_rate(valute):
	"""Обрабатывает необходимые операции c выбранной валютой"""
	answer_rate = requests.get('https://api.coingate.com/v2/rates/merchant')
	cross_usd = answer_rate.json()['USDT']
	rub_usd = float(cross_usd['RUB'])

	answer_cur_name = requests.get('https://api.coingate.com/v2/currencies')
	cur_name = answer_cur_name.json()

	global currency_name_dict
	currency_name_dict = {}
	for el in cur_name:
		# print(el['title'], el['symbol'])
		currency_name_dict[el['symbol']] = el['title']
	# print(currency_name_dict)

	rate_list = []
	for el in cross_usd:
		rate_list.append(el)

	rub_rate = {}
	for el in rate_list:
		rub_el = rub_usd / float(cross_usd[el])
		rub_rate[el] = rub_el

	if valute.upper() in currency_name_dict.keys():
		answer_rate = round(rub_rate[valute.upper()], 4)
		# answer_cur = currency_name_dict[valute.upper()]
		return f'{currency_name_dict[valute.upper()]} = {answer_rate} ₽'


def city_check(city):
	"""Проверяет существование города"""
	url_check = requests.get(f'https://nominatim.openstreetmap.org/search.php?city={city}&format=jsonv2')
	if not url_check.json():
		return False
	else:
		return True


def wright_db(user_log):
	with open('log.txt', 'a',
	          encoding='utf8') as f:  # не забыть, что повторное выполнение кода приводит к дозаписи(!) в файл
		f.write(f'{user_log}\n')


'''Данный модуль отвечает за парсинг: обрабатывает поток ссылок из Я.Новостей на конечные сайты СМИ, вытягивает из 
них ссылки на 5 последних новостей и записывает их в файл '''


def short_link(string):
    '''Вспомогательная функция: вытягивает из url-ссылок на сми короткие наименования сми'''
    # делает, что нужно, но почему-то сохраненные названия приводят к конфликтам при присвоении их к имени файла
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

        new_string = string[start:end]
        print(new_string)
    elif flag == 1:
        start = string.find('.')
        start = start + 1
        end = string.rfind('.')

        new_string = string[start:end]
        return new_string


def get_smi_links(smi_link):
    '''Основная функция для парсинга - получает ссылку на сми и вытягивает из неё (пока) список 5 статей'''
    # список статей записывается в файлы на винте, имя файла - имя сми
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
    # print(result)
    # url = result[17]
    # mail = result[18]
    # cite = short_link(result[17])

    links = []
    for el in result[19:24]:
        links.append(el)
    # os.remove("links.txt")

    with open(f'articles\\{smi_link[27:]}.txt', 'w', encoding='utf8') as f:
        # f.write(f'mail: {mail}')
        # f.write('\n')
        # f.write(f'site: {url}')
        # f.write('\n')
        # f.write(f'articles:\n')
        for el in links:
            f.write(f'{el}\n')


'''Данный модуль отвечает за формирование сводной базы статей, спарсенных в последний раз'''
# Из этой базы бот будет тащить запросы, отсюда будут формироваться словари пользовательских предпочтений"

def get_fresh_smi_json():
	'''Собирает результаты парсинга отдельных сайтов в сводный словарь и помещает в специальный json-файл'''
	today_links = []
	filenames_list = glob.glob("articles\\*.txt") # сохраняет в список файлы в директории articles с расширением *.txt
	# print(filenames_list)
	for file in filenames_list:
		with open(f'{file}', 'r', encoding='utf8') as f:
			templist = [] # Временный список для хранения ссылок по каждому сми
			today_smi_list = {}
			for line in f:
				templist.append(line.strip('\n').strip())
			# print(templist)
			today_smi_list['smi'] = file.lstrip('articles\\').rstrip('.txt')
			today_smi_list['articles'] = templist
			today_links.append(today_smi_list)
	with open('today_links_db.txt', 'w', encoding='utf8') as f:
		json.dump(today_links, f)


def get_smi_compilation(number=3):
	'''Генерирует заданное количество призвольных статей, хранящихся в json-файле today_links_db'''
	with open('today_links_db.txt', 'r', encoding='utf8') as f:
		json_file = json.load(f)

	articles_for_choise = []
	for smi in json_file:
		common_result = smi['articles'][:1][0] # в дальнейшем здесь  использовать переменную для задания общего количества выборки статей по одному сми
		articles_for_choise.append(common_result)
	random_final_article = random.choices(articles_for_choise, k=number)
	return random_final_article


# подключаемся к телеграму
bot = telebot.TeleBot(token=token)
users = {}


@bot.message_handler(commands=['start'])
def start(message):
	user = message.chat.id
	start_text = 'Чтобы начать, достаточно прислать боту свои координаты, ввести название города или код валюты (' \
	             'например, USD, EUR, TRY) '
	bot.send_message(user, start_text)


@bot.message_handler(commands=['help'])
def help(message):
	user = message.chat.id
	help_text = 'Поделишься своими координатами - получишь целую подборку,\nзапросишь город - вышлю прогноз погоды,' \
	            '\nа если валюту - свежие данные курса.\n\nГорода понимаю на любом языке, курс валют - только по ' \
	            'стандартным трёхбуквенным аббревиатурам (USD, EUR, CNY), но в любом регистре.\n\nПотихоньку научусь ' \
	            'большему - какие мои годы! '
	bot.send_message(user, help_text)


@bot.message_handler(content_types=['text'])
def guess_answer(message):
	"""Функция, которая пытается угадать из текста, что хочет пользователь: валюту или погоду"""
	#     # content_types=['text'] - сработает, если нам прислали текстовое сообщение
	#     # message - входящее сообщение
	user = message.chat.id  # id автора сообщения
	answer = message.text  # текст сообщения

	if answer.upper() in currency_name_dict.keys():
		currency_answer = currency_rate(answer)
		bot.send_message(user, currency_answer)
	elif city_check(answer.lower()):
		weather_answer = what_weather(answer)
		bot.send_message(user, weather_answer)
	else:
		bot.send_message(user, 'Не смог понять ваше сообщение: умею работать с координатами, городами и курсами валют/криптовалют. А у вас какая-то чушь, бумажки или компот')


@bot.message_handler(content_types=['location'])
def handle_loc(message):
	user = message.chat.id  # id автора сообщения
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	coord_dict = message.location
	default_currency = 'USD'
	coord = (coord_dict.latitude, coord_dict.longitude)
	reverse = partial(geolocator.reverse, language="ru")
	address = reverse(coord).raw['address']
	country = address['country']
	city = address['city']
	district = address['city_district']
	street = address['road']
	flat = address['house_number']
	bot.send_message(user, f'Доброе утро, {message.from_user.first_name} {message.from_user.last_name},\nболее '
	                       f'известный в сети как {message.from_user.username}')
	bot.send_message(user, f'Готовлю подборку главного для тебя, жителя человеческого поселения {city}, {country}')
	bot.send_message(user, f'Погодка сегодня у тебя такая:\n {what_weather(city)}')
	bot.send_message(user, f'Биржевой курс ихних бумажек:\n {currency_rate(default_currency)}')
	bot.send_message(user, f'Случайная подборка новостей для тебя:\n')
	for number in range(3):
		bot.send_message(user, {get_smi_compilation()[number-1]})
	bot.send_message(user, f'Вы держитесь здесь, вам всего доброго, хорошего настроения и здоровья!')
	user_log = [user, now, message.from_user.username, message.from_user.first_name, message.from_user.last_name, coord, country, city, district, street, flat]
	print(user_log)
	wright_db(user_log)


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
	user_id = message.chat.id
	users[user_id] = message.text


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
	try:
		users.pop(message.chat.id)
	except:
		pass

while True:
	try:
		bot.polling(none_stop=True)
	except:
		pass


