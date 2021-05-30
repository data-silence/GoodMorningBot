import glob
import os
import json
import random

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



# get_smi_compilation()


