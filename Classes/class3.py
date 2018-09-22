# Задание 4.1

myspreadsheet ="""Subject,Height,Occupation
1,74.37000326528938,Psychologist
2,67.49686206937491,Psychologist
3,74.92356434760966,Psychologist
4,64.62372198999978,Psychologist
5,67.76787900026083,Linguist
6,61.50397707923559,Psychologist
7,62.73680961908566,Psychologist
8,68.60803984763902,Linguist
9,70.16090500135535,Psychologist
10,76.81144438287173,Linguist"""

def csv_f(myspreadsheet):
    data_list = []
    my_lines = myspreadsheet.splitlines()
    datalines = my_lines[1:]
    for line in datalines:
        cells = line.split(',')
        cells[0] = int(cells[0])
        cells[1] = float(cells[1])
        data_list.append(cells)
    return data_list

csv_f(myspreadsheet)

#Задание 4.3
def dic_f(data_list):
    my_d = {}
    for list_el in data_list:
        if list_el[2] in my_d:
            my_d[list_el[2]] += 1
        else:
            my_d[list_el[2]] = 1
    print(my_d)
    return my_d

dic_f(csv_f(myspreadsheet))

import json

json_string = """			{
	"organisation": "HSE",
	"students": [{
			"first_name": "Maria",
			"last_name": "Ivanova",
			"group": "1"
		},
		{
			"first_name": "Yana",
			"last_name": "Petrova",
			"group": "2"
		},
		{
			"first_name": "Olga",
			"last_name": "Sidorova",
			"group": "3"
		}
	],
	"country": "Russia",
	"founded": 1992,
	"members": 27000,
	"url": "www.hse.ru"
}"""
data = json.loads(json_string)
print(type(data))
