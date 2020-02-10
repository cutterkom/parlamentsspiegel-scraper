# source venv/bin/activate

# collect links from overview pages

import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import numpy
import pandas as pd

# the scripts queries Parlementsspiegel twice: Once for searchwords, another time for keywords

SEARCHWORDS = "input/searchwords.csv"
KEYWORDS = "input/keywords.csv"
OUTPUT_FILE = "input/data/links_beratungsstand.csv"
BASE_URL = "https://www.parlamentsspiegel.de/sites/parlamentsspiegel/home/suchergebnisseparlamentsspiegel.html"


def load_querywords(INPUT_FILE, list_querywords):
	ifile  = open(INPUT_FILE, "r",)
	reader = csv.reader(ifile)
	next(reader)
	for row in reader: # each row is a list
		list_querywords.append(row)
	ifile.close()
	return(list_querywords)

# def save_csv(OUTPUT_FILE, list_links, queryword):
# 	print("dsafdasfasdf " + queryword[0])
# 	dict = {'queryword': queryword[0], 'links': list_links}
# 	df = pd.DataFrame(dict) 
# 	# saving the dataframe 
# 	df.to_csv('file1.csv') 
def save_csv(OUTPUT_FILE, list_links, queryword):
	#rows = zip(list_links, queryword)
	with open(OUTPUT_FILE, 'w') as f:
		writer = csv.writer(f, dialect="excel", quoting = csv.QUOTE_ALL)
		# for row in rows:
		# 	writer.writerow(row)
		keys = ["link"]#, "queryword"]
		writer.writerow(keys)
		for item in list_links:
			writer.writerow([item])

# def save_csv(OUTPUT_FILE, list_links, queryword):
# 	print("dsafdasfasdf " + queryword[0])
# #	rows = zip(list_links, queryword)
# 	with open(OUTPUT_FILE, 'w') as f:
# 		writer = csv.writer(f, dialect="excel", quoting = csv.QUOTE_ALL)
# 		# for row in rows:
# 		# 	writer.writerow(row)
# 		keys = ["link", "queryword"]
# 		writer.writerow(keys)
# 		for item in list_links:
# 			writer.writerow([item, queryword[0]])

def get_overview(BASE_URL, queryword):
	
	if queryword is searchword:
		url = BASE_URL + "?db=psakt&vir=alle&suchbegriff=" + queryword[0] + "&sortierung=dat_desc&verknuepfung=and"
	elif queryword is keyword:
		url = BASE_URL + "?db=psakt&vir=alle&schlagwort=" + queryword[0] + "&sortierung=dat_desc&verknuepfung=and"
	else:
		url = BASE_URL    

	# get content from url
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	# get link of last link in pagination
	# there is m=xxx: indicates the pagination
	# every page has 50 entries
	pagination = soup.find_all("ul", {"class": "paging"})[0].find("li", {"class": "last"})

	if pagination:
		pagination = pagination.find_all("a")[0]['href']
		pagination = re.search(r"(?<=m=)\d+", pagination)[0]
		print("pages: " + pagination)
		pagination_input = numpy.arange(1, int(pagination)+1, 50)
	else:
		pagination_input = [1]
		print("entries under 50 ")

	# get html pages 
	for i in pagination_input:
		url_paginated = url + "&m=" + str(i)
		page = requests.get(url_paginated)
		soup = BeautifulSoup(page.content, 'html.parser')
		# save html file
		with open("input/html/overview/" + queryword[0] + "_" + str(i) + ".html", "w") as file:
			file.write(str(soup))

		# get all link zu detailseiten
		links = soup.find_all("a", {"class": "beratungsstand"})#

		# man muss da so blöd drüber loopen um sie in die liste zu bekommen
		for link in links:
			if link.has_attr('href'):
				beratungslinks.append(link["href"])
				#print(link)
		print("vorm speichern " + queryword[0])
		print(len(beratungslinks))
		save_csv(OUTPUT_FILE, beratungslinks, queryword)    

# init lists and load querywords
searchwords = []
searchwords = load_querywords(SEARCHWORDS, searchwords)
# searchwords = searchwords[1:2]

keywords = []
keywords = load_querywords(KEYWORDS, keywords)
# keywords = keywords[1:2]

beratungslinks = []

for searchword in searchwords:
	print("searchword: " + searchword[0])
	get_overview(BASE_URL, searchword)

for keyword in keywords:
	print("keyword: " + keyword[0])
	get_overview(BASE_URL, keyword)