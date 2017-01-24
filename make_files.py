import os
from operator import itemgetter
import re
import numpy as np
import mlp

def make_sets(matches, home_team_dict, away_team_dict):
	inputs = []
	targets = []
	
	for match in matches:
		c_train = []
		c_traint = [int(match[3])-int(match[4])]
		""" CLASSIFICATION
		if int(match[3]) > int(match[4]):
			c_traint = [1,0,0]
		elif int(match[3]) < int(match[4]):
			c_traint = [0,0,1]
		else:
			c_traint = [0,1,0]
		"""
		home_team_home_matches = home_team_dict[match[1]]
		home_team_away_matches = away_team_dict[match[1]]
		away_team_home_matches = home_team_dict[match[2]]
		away_team_away_matches = away_team_dict[match[2]]

		home_team_matches = []
		home_team_matches.extend(home_team_home_matches)
		home_team_matches.extend(home_team_away_matches)
		home_team_matches = sorted(home_team_matches, key = itemgetter(0)) 

		away_team_matches = []
		away_team_matches.extend(away_team_away_matches)
		away_team_matches.extend(away_team_away_matches)
		away_team_matches = sorted(away_team_matches, key = itemgetter(0))

		for hm in home_team_home_matches:
			if hm[0] == match[0]:
				hh_index = home_team_home_matches.index(hm)
		for m in home_team_matches:
			if m[0] == match[0]:
				ht_index = home_team_matches.index(m)
		for oam in away_team_away_matches:
			if oam[0] == match[0]:
				oa_index = away_team_away_matches.index(oam)
		for om in away_team_matches:
			if om[0] == match[0]:
				om_index = away_team_matches.index(om)

		home_team_form = 0
		for i in range(ht_index+1, min(ht_index+10,len(home_team_matches))):
			home_team_form += int(home_team_matches[i][3]) - int(home_team_matches[i][4]) #home/away goal difference
			
		c_train.append(home_team_form)

		home_team_home_form = 0
		for i in range(hh_index+1, min(hh_index+5,len(home_team_home_matches))):
			home_team_home_form += int(home_team_home_matches[i][3]) - int(home_team_home_matches[i][4])
		c_train.append(home_team_home_form)

		home_team_form_against_opposition = 0
		matches_counted = 0
		for i in range(ht_index+1, len(home_team_matches)):
			if matches_counted > 4:
				break
			if home_team_matches[i][2] == match[2]:
				home_team_form_against_opposition += int(home_team_matches[i][3]) - int(home_team_matches[i][4])
		c_train.append(home_team_form_against_opposition)

		opposition_form = 0
		for i in range(om_index+1, min(om_index+10,len(away_team_matches))):
			opposition_form += int(away_team_matches[i][4]) - int(away_team_matches[i][3])

		c_train.append(home_team_form)

		opposition_away_form = 0
		for i in range(oa_index+1, min(oa_index+5,len(away_team_away_matches))):
			opposition_away_form += int(away_team_away_matches[i][4]) - int(away_team_away_matches[i][3])
		c_train.append(opposition_away_form)

		inputs.append(c_train)
		targets.append(c_traint)

	return inputs,targets




all_matches = []

for filename in os.listdir('Stash'):
	file = open('Stash/' + filename,'r')
	season = file.read().rstrip().split('\n')
	all_matches.extend(season)
	file.close()
i=0
while i < len(all_matches):
	if len(all_matches[i]) < 5:
		del all_matches[i]
	i+=1



i=0
while i < len(all_matches): #split matches and get rid of invalid rows
	all_matches[i] = all_matches[i].split(',')
	all_matches[i] = all_matches[i][:6]
	del all_matches[i][0]
	if len(all_matches[i]) != 5:
		del all_matches[i]
		continue
	i+=1

i=0
while i < len(all_matches):
	try:
		if all_matches[i][0] == 'Date':
			del all_matches[i]
			continue
		elif all_matches[i][3] == '' or all_matches[i][3] == ' ': #some garbage, not really sure...
			del all_matches[i]
			continue
	except IndexError as e:
		del all_matches[i]
		continue
	i+=1

i=0
while i < len(all_matches):
	try:
		date_arr = re.split('\-|/',all_matches[i][0])
		if len(date_arr) < 3:
			del all_matches[i]
			continue
		if int(date_arr[2]) < 19:
			date_arr[2] = '20' + date_arr[2]
		elif int(date_arr[2]) > 90 and int(date_arr[2]) < 100:
			date_arr[2] = '19' + date_arr[2]
		date_int = date_arr[2] + date_arr[1] + date_arr[0]
		all_matches[i][0] = int(date_int)
	except IndexError as e:
		print(all_matches[i], i)
		del all_matches[i]
		continue
	i+=1

all_matches_by_date = sorted(all_matches, key = itemgetter(0))
all_matches_by_date.reverse()

teams = []

for i in range(len(all_matches_by_date)):
	if all_matches_by_date[i][1] not in teams:
		teams.append(all_matches_by_date[i][1])
	elif all_matches_by_date[i][2] not in teams:
		teams.append(all_matches_by_date[i][2])


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