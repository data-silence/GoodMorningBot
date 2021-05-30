import requests



zap = 'eur'
answ = market_rate(zap)
print(answ)


def currency_rate(valute):
	"""Обрабатывает необходимые операции c выбранной валютой"""
	cbr = (requests.get('https://www.cbr-xml-daily.ru/daily_json.js')).json()
	currency_list = []

	for currency in cbr['Valute']:
		currency_list.append(currency)
	if valute.upper() in currency_list:
		delta = round(100 * (cbr['Valute'][valute.upper()]['Value'] - cbr['Valute'][valute.upper()]['Previous']) /
		              cbr['Valute'][valute.upper()]['Previous'], 2)
		currency = cbr['Valute'][valute.upper()]['Value']
		return f'{valute.upper()} {currency} ₽, ∆ {delta}% today'
	else:
		return 'Вы ошиблись, такой валюты не существует'