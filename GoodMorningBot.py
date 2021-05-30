import telebot
import requests
from functools import partial
from geopy.geocoders import Nominatim
import json
import datetime

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows; U; WinNT; en; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable")
token = "1864998452:AAGI9AWWy9kiExZWSM5fqUv8XcnNXiRNR8s"

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
	# db = {}
	# db['user'] = user
	# db['first_name'] = first_name
	# db['last_name'] = last_name
	# db['city'] = city
	# db['country'] = country
	# db['coord'] = coord
	with open('log.txt', 'a',
	          encoding='utf8') as f:  # не забыть, что повторное выполнение кода приводит к дозаписи(!) в файл
		f.write(f'{user_log}\n')
		# json.dump(temp_list, f)


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


@bot.message_handler(content_types=['location'])
def handle_loc(message):
	user = message.chat.id  # id автора сообщения
	# global user
	# global message.from_user.first_name
	# global message.from_user.last_name
	# global city
	# global country
	# global coord
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
	bot.send_message(user, f'Вы держитесь здесь, вам всего доброго, хорошего настроения и здоровья!')
	# wright_db(user, message.from_user.first_name, message.from_user.last_name, city, country, coord)
	user_log = [user, now, message.from_user.username, message.from_user.first_name, message.from_user.last_name, coord, country, city, district, street, flat]
	print(user_log)
	wright_db(user_log)

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


# print(users)
# поллинг - вечный цикл с обновлением входящих сообщений
while True:
	try:
		bot.polling(none_stop=True)
	except:
		pass

# print(users)
# help
# print(f'Какая валюта вас интересует? Введите общепринятый код валюты из трех латинских букв:')
# print(f'Все доступные валюты здесь: {currency_list}')
