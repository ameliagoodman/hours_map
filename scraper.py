import requests
import sys
import pprint
import os
import psycopg2
from geopy.geocoders import Nominatim
import datetime


now = datetime.datetime.now()
years = [str(now.year)]
months = [str(now.month)]

date = {}


for year in years:
	date[year] = {}
	for month in months:
		archive = {}
		payload = {'api-key': "3e0a481794454b048bd6e0ff9af36de7"}
		url = "https://api.nytimes.com/svc/archive/v1/" + year + "/" + month + ".json"
		try:
			r = requests.get(url, params=payload)
		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)
		if r.status_code == 429:
			print "API limit exceeded"
			sys.exit(1)
		if "response" in r.json().keys():
			if "docs" in r.json()['response'].keys():
				data = r.json()['response']['docs']
				for article in data:
					if article['headline']:
						keys = article['headline'].keys()
						if 'kicker' in  article['headline'].keys():
							if article['headline']['kicker']:
								if article['headline']['kicker'] == '36 Hours' or article['headline']['kicker'] == '36 HOURS':
									link = article['web_url']
									locationFound = False
									for item in article['keywords']:
										if item['value'] != 'Travel and Vacations' and not locationFound:
											location = item['value']
											locationFound = True
									if locationFound:
										archive[location] = link
								# to adjust for weird 2006 articles
								elif '36 Hours' in article['headline']['kicker']:
									link = article['web_url']
									locationFound = False
									for item in article['keywords']:
										if item['value'] != 'Travel and Vacations' and not locationFound:
											location = item['value']
											locationFound = True
									archive[location] = link
								# to adjust for weird 2015 articles
								elif article['headline']['kicker'] == 'Weekend Guide':
									link = article['web_url']
									location = ""
									locationFound = False
									for item in article['keywords'] :
										if item['is_major'] == 'Y' and item['name'] == 'glocations' and not locationFound:
											location = item['value']
											locationFound = True
									archive[location] = link
								# to adjust for weird 2005 articles
								elif '36 Hours' in article['headline']['main']:
									link = article['web_url']
									if "|" in article['headline']['main']:
										find_location = article['headline']['main'].split("|")
										location = find_location[1].strip()
										archive[location] = link
						# to adjust for 2014 articles
						elif 'content_kicker' in  article['headline'].keys():
							 if article['headline']['content_kicker'] == '36 Hours':
							 	link = article['web_url']
								locationFound = False
								for item in article['keywords']:
									if item['value'] != 'Travel and Vacations' and item['name'] != 'subject' and not locationFound:
										location = item['value']
										locationFound = True
								archive[location] = link
						# to adjust for 2006 articles
						# elif 'main' in article['headline'].keys():
						# 	if '36 Hours' in article['headline']['main']
		date[year][month] = archive
		# print "scraped month " + month + " of year " + year + "."
		
# pprint.pprint(date)
# print len(date)


# connect to db
DATABASE_URL = os.environ['DATABASE_URL']


conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
geolocator = Nominatim()

# add to db
for year in date:
	for month in date[year]:
		for location in date[year][month]:
			lat_lon = geolocator.geocode(location)
			if lat_lon:
				lat = lat_lon.latitude 
				lon = lat_lon.longitude
			else:
				location2 = location.split("(")
				lat_lon = geolocator.geocode(location2)
				if lat_lon:
					lat = lat_lon.latitude
					lon = lat_lon.longitude
				else: 
					continue
			sql = "INSERT INTO locations(location, link, pub_date, lat, long) VALUES(%s, %s, %s, %s, %s)"
			try:
				pub_date = month + "-" + year
				cur.execute(sql, (location, date[year][month][location], pub_date, lat, lon,))
				conn.commit()
				# print "added %s to db" %location
			except (Exception, psycopg2.DatabaseError) as error:
				print(error)
				conn.rollback()
	
# close db connection
if conn is not None:
	cur.close()
	conn.close()