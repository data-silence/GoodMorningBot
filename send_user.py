import glob
import os

today_links = []

filenames_list = glob.glob("articles\\*.txt")
for file in filenames_list:
	with open(f'{file}', 'r', encoding='utf8') as f:
		for line in f:
			print(line.strip('\n').strip())
			# result.append(line.strip('\n').strip())

