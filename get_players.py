from multiprocessing import Pool
import urllib.request
import json
from bs4 import BeautifulSoup as bs
import re

def getMMR(name):
	try:
		url_name = "http://na.op.gg/summoner/ajax/mmr/summonerName=" + name
		url = urllib.request.urlopen(url_name)
		data = url.read()
		parsed_data = bs(data, "lxml")
		num = ""
		for item in re.findall('\d+', parsed_data.findAll("td", {"class": "MMR"})[0].text): num += item
		num = int(num)
		return num
	except:
		return 0

if __name__ == '__main__':
	players_file = open("players.txt", "r")
	player_names = players_file.readlines()
	player_names = [x.strip() for x in player_names]

	pool = Pool(20)
	ranks = pool.map(getMMR, player_names)
		
	with open('rankings.txt', 'w') as file:
		for i in range(len(player_names)):
			file.write(player_names[i] + "," + str(ranks[i]) + "\n")