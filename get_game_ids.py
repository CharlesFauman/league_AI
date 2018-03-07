# imports
import urllib.parse
import urllib.request
import json
import csv
import os

if __name__ == '__main__':
	rankings_file = csv.DictReader(open("rankings.txt", "r"))
	player_rankings = dict()
	for row in rankings_file:
		if(row['mmr'] != '0'):
			player_rankings[row['name']] = int(row['mmr'])
	start_index = 842
	end_index = start_index + 50
	sorted_players = sorted(player_rankings, key=player_rankings.get, reverse=True)[start_index:end_index]
	
	game_ids_filepath = 'game_ids.txt'
	game_ids = set()
	if(os.path.isfile(game_ids_filepath)):
		with open(game_ids_filepath, 'r') as file:
			game_ids = file.readlines()
			game_ids = set([int(x.strip()) for x in game_ids])
	
	site = "https://na1.api.riotgames.com"
	key = "?api_key=RGAPI-1249e1f6-40ec-4cad-ae60-1d95b9666ca0"
	index = start_index
	for player in sorted_players:
		try:
			summoner_urlname = site+"/lol/summoner/v3/summoners/by-name/" + player + key
			print(summoner_urlname)
			summoner_url = urllib.request.urlopen(summoner_urlname)
			summoner_data = summoner_url.read()
			summoner_encoding = summoner_url.info().get_content_charset('utf-8')
			summoner = json.loads(summoner_data.decode(summoner_encoding))
			summoner_id = summoner['accountId']
			
			matches_urlname = site + "/lol/match/v3/matchlists/by-account/" + str(summoner_id) + key
			matches_url = urllib.request.urlopen(matches_urlname)
			matches_data = matches_url.read()
			matches_encoding = matches_url.info().get_content_charset('utf-8')
			matches = json.loads(matches_data.decode(matches_encoding))['matches']
			for match in matches:
				if(match['queue'] == 420):
					game_ids.add(match['gameId'])
			index += 1
		except Exception as e:
			print(e)
			break
			
	with open(game_ids_filepath, 'w') as file:
		for id in game_ids:
			file.write(str(id) + "\n")
			
	print(index)