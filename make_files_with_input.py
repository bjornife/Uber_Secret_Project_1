import os
from operator import itemgetter
import re
import numpy as np
import mlp
import urllib.request

def make_files(matches_to_check):

	all_seasons = []
	all_matches = []
	for filename in os.listdir('../../Football_Data/Stash'):
		file = open('../../Football_Data/Stash/' + filename,'r')
		season = file.read().rstrip()
		all_seasons.append(season)
		file.close()

	for season in all_seasons:
		season = season.split('\n')
		for i in range(0,len(season)):
			season[i] = season[i].split(',')
		if "HST" in season[0]:
			has_odds = False
			date_index = season[0].index("Date")
			ht_index = season[0].index("HomeTeam")
			at_index = season[0].index("AwayTeam")
			home_goal_index = season[0].index("FTHG")
			away_goal_index = season[0].index("FTAG")
			hst_index = season[0].index("HST")
			ast_index =  season[0].index("AST")
			
			home_odds_index = -1
			draw_odds_index = -1
			away_odds_index = -1

			if "BWH" in season[0]:
				has_odds = True 
				home_odds_index = season[0].index("BWH")
				draw_odds_index = season[0].index("BWD")
				away_odds_index = season[0].index("BWA")

			for i in range(1,len(season)):
				if season[i][hst_index] != '' and season[i][ast_index] != '':
					match = [season[i][date_index],season[i][ht_index],season[i][at_index],season[i][home_goal_index],season[i][away_goal_index],season[i][hst_index],season[i][ast_index]]
					if has_odds:
						match.extend([season[i][home_odds_index],season[i][draw_odds_index],season[i][away_odds_index]])
					all_matches.append(match)

	for i in range(0,len(all_matches)):
		date_arr = re.split('\-|/',all_matches[i][0])
		if int(date_arr[2]) < 19:
			date_arr[2] = '20' + date_arr[2]
		elif int(date_arr[2]) > 90 and int(date_arr[2]) < 100:
			date_arr[2] = '19' + date_arr[2]
		date_int = date_arr[2] + date_arr[1] + date_arr[0]
		all_matches[i][0] = int(date_int)

	all_matches_by_date = sorted(all_matches, key = itemgetter(0))
	all_matches_by_date.reverse()

	teams = []

	for i in range(len(all_matches_by_date)):
		if all_matches_by_date[i][1] not in teams:
			teams.append(all_matches_by_date[i][1])
		elif all_matches_by_date[i][2] not in teams:
			teams.append(all_matches_by_date[i][2])

	todays_matches = []

	for match in matches_to_check:
		if match[0] in teams and match[1] in teams:
			todays_matches.append(match)

	home_team_dict = dict(zip(teams,([] for i in range(len(teams))))) #damn son, value arrays sorted by date
	away_team_dict = dict(zip(teams,([] for i in range(len(teams)))))

	for match in all_matches_by_date: #make one dictionary based on the home teams, and one based on away teams
		home_team_dict[match[1]].append(match)
		away_team_dict[match[2]].append(match)

	with open('home_team_dict.txt','w') as home_dict_file:
		home_dict_file.write(str(home_team_dict))

	with open('away_team_dict.txt','w') as away_dict_file:
		away_dict_file.write(str(away_team_dict))

	with open('all_matches.txt','w') as all_matches_file:
		all_matches_file.write(str(all_matches))

	with open('todays_matches.txt','w') as todays_matches_file:
		todays_matches_file.write(str(todays_matches))



response = 	urllib.request.urlopen('http://www.sportstats.com/soccer/matches/')

url_string = str(response.read())
teams = re.finditer('(/detail/.*?>)(.*?)<', url_string)

matches_to_check = []
switch = False
team_touple = []
for item in teams:
	team_touple.append(item.group(2))
	if switch:
		matches_to_check.append(team_touple)
		team_touple = []
		switch = False
	else:
		switch = True

make_files(matches_to_check)