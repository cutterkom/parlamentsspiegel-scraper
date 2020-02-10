# source venv/bin/activate

import pandas as pd
from bs4 import BeautifulSoup
import re
import os.path
import requests
import time


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()

INPUT_FILE = "input/data/links_beratungsstand.csv"
BASE_URL = "https://www.parlamentsspiegel.de"
OUTPUT_DIR = "input/html/beratungsstand/"

# load links to pages
df = pd.read_csv(INPUT_FILE)
links = df["link"].tolist()
l = len(links)

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

for i, link in enumerate(links):
	url = BASE_URL + link
	id = re.search("id=.*", link).group(0)
	id = re.sub("id=", "", id)
	id = re.sub(r"\/", "", id)

	fname = id + ".html"
	if os.path.isfile(OUTPUT_DIR + fname):
		print("already saved")
	else: 
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')	
		with open(OUTPUT_DIR + fname, "w", encoding = "utf-8") as f:
			f.write(str(soup))
		print(id + " saved")
	# Update Progress Bar
	time.sleep(0.1)
	printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)