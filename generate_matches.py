# imports
import urllib.parse
import urllib.request
import json
import csv
import os
import sys

def get_match(game, player_rankings):
	participant_MMRs = dict()
	for player in game['participantIdentities']:
		name = urllib.parse.quote_plus(''.join(c.lower() for c in player['player']['summonerName'] if not c.isspace()))
		if name in player_rankings:
			participant_MMRs[player['participantId']] = player_rankings[name]
	if(len(participant_MMRs) != 10):
		print(participant_MMRs)
		return False

	team_win = 200
	for item in game['teams']:
		if item['teamId'] == 100:
			if item['win'] == 'Win':
				team_win = 100
		break

	match = dict()
	winteam = list()
	loseteam = list()
	for participant in game['participants']:
		player_info = dict()
		player_info['championId'] = participant['championId']
		player_info['MMR'] = participant_MMRs[participant['participantId']]
		if participant['teamId'] == team_win:
			winteam.append(player_info)
		else:
			loseteam.append(player_info)
	
	if(not (len(winteam) == 5 and len(loseteam) == 5)):
		return False	
			
	match['win'] = winteam
	match['lose'] = loseteam
	
	return match


if __name__ == '__main__':
	rankings_file = csv.DictReader(open("rankings.txt", "r"))
	player_rankings = dict()
	for row in rankings_file:
		if(row['mmr'] != '0'):
			player_rankings[row['name']] = int(row['mmr'])

	matches_filepath = "matches.json"
	matches = dict()
	if(os.path.isfile(matches_filepath)):
		with open(matches_filepath, 'r') as file:
				matches = json.load(file)
	
	game_ids_filepath = "game_ids.txt"
	game_ids = set()
	if(os.path.isfile(game_ids_filepath)):
		with open(game_ids_filepath, 'r') as file:
			game_ids = file.readlines()
			game_ids = set([str(x.strip()) for x in game_ids])
	else:
		sys.exit()
		
	bad_game_ids_filepath = "bad_game_ids.txt"
	bad_game_ids = set()
	if(os.path.isfile(bad_game_ids_filepath)):
		with open(bad_game_ids_filepath, 'r') as file:
			bad_game_ids = file.readlines()
			bad_game_ids = set([str(x.strip()) for x in bad_game_ids])
	
	site = "https://na1.api.riotgames.com"
	key = "?api_key=RGAPI-1249e1f6-40ec-4cad-ae60-1d95b9666ca0"
	while game_ids:
		game_id = game_ids.pop()
		print(str(game_id) + ": ", end = '')
		if(game_id in bad_game_ids):
			print("bad id")
			continue
		if(game_id in matches):
			print("satisfied")
			continue
		game_urlname = site + "/lol/match/v3/matches/" + str(game_id) + key
		try:
			game_url = urllib.request.urlopen(game_urlname)
			game_data = game_url.read()
			game_encoding = game_url.info().get_content_charset('utf-8')
			game = json.loads(game_data.decode(game_encoding))
			match = get_match(game, player_rankings)
			if(match != False):
				matches[game_id] = match
				print(match)
			else:
				print("bad match")
				bad_game_ids.add(game_id)
		except Exception as e:
			game_ids.add(game_id)
			print(e)
			break
	
	print("matches: " + str(len(matches)))
	with open(matches_filepath, 'w') as file:
		json.dump(matches, file, indent=2)
		
	with open(bad_game_ids_filepath, 'w') as file:
		for id in bad_game_ids:
			file.write(str(id) + "\n")
	
	with open(game_ids_filepath, 'w') as file:
		for id in game_ids:
			file.write(str(id) + "\n")
	
	