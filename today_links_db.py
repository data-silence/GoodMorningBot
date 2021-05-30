import glob
import os

today_links = []

filenames_list = glob.glob("articles\\*.txt")
for file in filenames_list:
	with open(f'{file}', 'r', encoding='utf8') as f:
		templist = []
		today_smi_list = {}
		for line in f:
			templist.append(line.strip('\n').strip())
		# print(templist)
		today_smi_list[templist[1[:3]]] = templist[1[6:]]
		today_links.append(today_smi_list)
print(today_links)
			# print(line[1])
			# result.append(line.strip('\n').strip())

