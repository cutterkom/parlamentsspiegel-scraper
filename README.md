# Parlamentsspiegel Scraper
 
 The [Parlamentsspiegel](https://www.parlamentsspiegel.de/home/einfache-suche.html) collects the federal parliamentary documentation of Germany. 

Unfortunately, the documents on Parlamentsspiegel lack consistent meta data. For example, they use weird abbreviations for the German federal states, like `SACA` for Sachsen-Anhalt. That's far away from common standards like [NUTS](https://en.wikipedia.org/wiki/NUTS) or [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166)... The translation between Parlamentsspiegel's weird country codes and more widely used codes can be found in `input/lookup_laender_ps.csv`

Also, the HTML structure has no well defined css classes, which makes the parsing a bit annoying.

The crawler is written in Python, the parsing in R.

## Setup

* create a virtual environment: `python3 -m venv env`
* activate it: `source env/bin/activate`
* install requirements: `pip3 install -r requirements.txt`

## Use it

### Define your search interest

1. Write your search words for the search input field in `input/searchwords.csv`
2. and the [official tags ("Schlagworte")](https://www.parlamentsspiegel.de/sites/parlamentsspiegel/home/indexeinblick.html) you're interested in `input/keywords.csv`

### Run scripts 

1. `01_get_overview.py`: to fetch all overview tables, which will be stored as `html` files in `input/html/overview/` and relevant links in `input/data/links_beratungsstand.csv`
2. `02_get_detailpages.py`: to get all the information for every single document, the resulting `html` files can be found in `input/html/beratungsstand/`
3. `03_parsing.R`: to free metadata and to get a csv file with parsed information, that can be found in `input/data/df.csv`

## To Do
- [ ] clear distiction between `input` and `output`
- [ ] automate folder creation
- [ ] improve metadata parsing
