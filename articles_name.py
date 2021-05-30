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

for url in parsing_url:
	print((url[27:]))