import pandas as pd
import json as js
import xlsxwriter
from urllib.request import Request, urlopen

def scrapeData(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/83.0'})
	web_byte = urlopen(req).read()
	webpage = web_byte.decode('utf-8')
	scrapedData = js.loads(webpage)
	return scrapedData 

#Obtaining the list of counties of North Carolina
county_list = scrapeData("https://er.ncsbe.gov/enr/20201103/data/county.txt?v=26-11-50")

#Obtaining the election dates
date_list = scrapeData("https://er.ncsbe.gov/enr/elections.txt?v=26-13-17")
election_dates = []
for i in date_list:
	dt = i["edt"]
	dt = list(dt.split("/"))
	if dt[2] > "2016":
		dt = dt[2:]+dt[:2]
		dt = "".join(dt)
		election_dates.append(dt)

row = []
for i in county_list:
	row.append([i['cnm'], i['bct'], i['rtl'], i['bpt'], i['ptl']])

for elecDate in election_dates:
	for n in range(len(county_list)):

		url="https://er.ncsbe.gov/enr/"+elecDate+"/data/results_"+str(n)+".txt"
		try:
			data = scrapeData(url)
		except:
			print("", end='#')
		entry = []

		dem = []
		rep = []
		for i in data:
			name = i['cnm']
			if name == "US PRESIDENT (VOTE FOR 1)" and i['pty'] == "DEM":
				dem.append(i['vct'])
				dem.append(i['pct'])
			if name == "US PRESIDENT (VOTE FOR 1)" and i['pty'] == "REP":
				rep.append(i['vct'])
				rep.append(i['pct'])

		row[n].extend(dem)
		row[n].extend(rep)

	df = pd.DataFrame(row, columns = ['CountyName', 'BallotsCast', 'OutOf', 'Turnout', 'No.OfPrecincts', 'DEM-PRES-VOTES', 'DEM-PRES-PERCENT', 'REP-PRES-VOTES', 'REP-PRES-PERCENT'])
	df.to_excel('TurnoutResults/PresedentialElectionTurnout'+elecDate+'.xlsx')