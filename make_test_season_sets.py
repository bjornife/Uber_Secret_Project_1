import numpy as np
from operator import itemgetter

def make_sets(matches, home_team_dict, away_team_dict, test_written = False):
	inputs = []
	targets = []
	
	matches_to_count = 75
	matches_covered = 0
	number_of_matches = len(matches)
	percent_done = 0
	for match in matches:

		matches_covered +=1
		if matches_covered == int(number_of_matches/10):
			percent_done +=10
			print("DATA ", percent_done, "% READY")
			matches_covered = 0

		c_train = []
		#c_traint = [int(match[3]) - int(match[4])]
		
		""" CLASSIFICATION """	

		if int(match[3]) > int(match[4]):
			c_traint = [1,0,0]
		elif int(match[3]) < int(match[4]):
			c_traint = [0,0,1]
		else:
			c_traint = [0,1,0]
		
		home_team_home_matches = home_team_dict[match[1]]
		home_team_away_matches = away_team_dict[match[1]]
		away_team_home_matches = home_team_dict[match[2]]
		away_team_away_matches = away_team_dict[match[2]]

		home_team_home_matches = sorted(home_team_home_matches, key = itemgetter(0))
		home_team_away_matches = sorted(home_team_away_matches, key = itemgetter(0))
		away_team_home_matches = sorted(away_team_home_matches, key = itemgetter(0))
		away_team_away_matches = sorted(away_team_away_matches, key = itemgetter(0))

		home_team_matches = []
		home_team_matches.extend(home_team_home_matches)
		home_team_matches.extend(home_team_away_matches)
		home_team_matches = sorted(home_team_matches, key = itemgetter(0)) 

		away_team_matches = []
		away_team_matches.extend(away_team_home_matches)
		away_team_matches.extend(away_team_away_matches)
		away_team_matches = sorted(away_team_matches, key = itemgetter(0))

		if not test_written:
			with open('trouble/home_team_home_matches.txt','w') as f1, open('trouble/home_team_away_matches.txt','w') as f2, open('trouble/away_team_home_matches.txt','w') as f3, open('trouble/away_team_away_matches.txt', 'w') as f4, open('trouble/home_team_matches.txt', 'w') as f5, open('trouble/away_team_matches.txt','w') as f6:
				f1.write(str(home_team_home_matches))
				f2.write(str(home_team_away_matches))
				f3.write(str(away_team_home_matches))
				f4.write(str(away_team_away_matches))
				f5.write(str(home_team_matches))
				f6.write(str(away_team_matches))
				test_written = True

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
		matches_counted = 0
		for i in range(max(0,ht_index-matches_to_count),ht_index):
			if home_team_matches[i][1] == match[1]:
				if home_team_matches[i][3] > home_team_matches[i][4]:
					home_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*3
				elif home_team_matches[i][3] == home_team_matches[i][4]:
					home_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			else:
				if home_team_matches[i][4] > home_team_matches[i][3]:
					home_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*3
				elif home_team_matches[i][4] == home_team_matches[i][3]:
					home_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			matches_counted +=1

		if matches_counted >= max(int(matches_to_count*0.6), 1): #using only samples with more than three matches in history
			home_team_form = home_team_form/matches_counted
			#home_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*(10-matches_counted)*1.5 #compensating for possible missing matches
			c_train.append(home_team_form)
		

		home_team_home_form = 0
		matches_counted = 0
		for i in range(max(0,hh_index-matches_to_count), hh_index):
			if home_team_home_matches[i][3] > home_team_home_matches[i][4]:
				home_team_home_form += (1/(np.log(max(0.01,matches_counted)) + 1))*3
			elif home_team_home_matches[i][3] == home_team_home_matches[i][4]:
				home_team_home_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			matches_counted +=1

		#home_team_home_form += (1/(np.log(max(0.01,matches_counted)) + 1))*(5-matches_counted)*2
		if matches_counted >= max(int(matches_to_count*0.6), 1):
			home_team_home_form = home_team_home_form/matches_counted
			c_train.append(home_team_home_form)

		home_team_goals_for = 0
		home_team_goals_against = 0
		matches_counted = 0
		for i in range(max(0,ht_index-matches_to_count),ht_index):
			if home_team_matches[i][1] == match[1]: #check if home team played the match at home
				home_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][3])
				home_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][4])
			else:
				home_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][4])
				home_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][3])
			matches_counted +=1
		
		#home_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*10-matches_counted
		#home_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*10-matches_counted

		if matches_counted >= max(int(matches_to_count*0.6), 1):
			home_team_goals_for = home_team_goals_for/matches_counted
			home_team_goals_against = home_team_goals_against/matches_counted
			c_train.append(home_team_goals_for)
			c_train.append(home_team_goals_against)

		home_team_shots_for = 0
		home_team_shots_against = 0
		matches_counted = 0
		for i in range(max(0,ht_index-matches_to_count),ht_index):
			if home_team_matches[i][1] == match[1]: #home team at home
				home_team_shots_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][5])
				home_team_shots_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][6])
			else:
				home_team_shots_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][6])
				home_team_shots_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(home_team_matches[i][5])
			
			matches_counted +=1
		
		#home_team_shots_for += (1/(np.log(max(0.01,matches_counted)) + 1))*(5-matches_counted)*5
		#home_team_shots_against += (1/(np.log(max(0.01,matches_counted)) + 1))*(5-matches_counted)*5
		if matches_counted >= max(int(matches_to_count*0.6), 1):
			home_team_shots_for = home_team_shots_for/matches_counted
			home_team_shots_against = home_team_shots_against/matches_counted
			c_train.append(home_team_shots_for)
			c_train.append(home_team_shots_against)

		#TODO: Implement intra-team form?

		away_team_form = 0
		matches_counted = 0
		for i in range(max(0,om_index-matches_to_count),om_index):
			if away_team_matches[i][1] == match[2]: #away team at home
				if away_team_matches[i][3] > away_team_matches[i][4]:
					away_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*3
				elif away_team_matches[i][3] == away_team_matches[i][4]:
					away_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			else:
				if away_team_matches[i][4] > away_team_matches[i][3]:
					away_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
				elif away_team_matches[i][4] == away_team_matches[i][3]:
					away_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			matches_counted +=1

		#away_team_form += (1/(np.log(max(0.01,matches_counted)) + 1))*(5-matches_counted)*1.5
		if matches_counted >= max(int(matches_to_count*0.6), 1):
			away_team_form = away_team_form/matches_counted
			c_train.append(away_team_form)

		away_team_away_form = 0
		matches_counted = 0
		for i in range(max(0,oa_index-matches_to_count), oa_index):
			if away_team_away_matches[i][4] > away_team_away_matches[i][3]:
				away_team_away_form += (1/(np.log(max(0.01,matches_counted)) + 1))*3
			elif away_team_away_matches[i][4] == away_team_away_matches[i][3]:
				away_team_away_form += (1/(np.log(max(0.01,matches_counted)) + 1))*1
			matches_counted +=1

		#away_team_away_form += (1/(np.log(max(0.01,matches_counted)) + 1))*5-matches_counted

		if matches_counted >= max(int(matches_to_count*0.6), 1):
			away_team_away_form = away_team_away_form/matches_counted
			c_train.append(away_team_away_form)

		away_team_goals_for = 0
		away_team_goals_against = 0
		matches_counted = 0
		for i in range(max(0,om_index-matches_to_count),om_index):
			if away_team_matches[i][1] == match[2]:#away team at home
				away_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][3])
				away_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][4])
			else:
				away_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][4])
				away_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][3])
			matches_counted +=1

		#away_team_goals_for += (1/(np.log(max(0.01,matches_counted)) + 1))*10-matches_counted
		#away_team_goals_against += (1/(np.log(max(0.01,matches_counted)) + 1))*10-matches_counted
		if matches_counted >= max(int(matches_to_count*0.6), 1):
			away_team_goals_for = away_team_goals_for/matches_counted
			away_team_goals_against = away_team_goals_against/matches_counted
			c_train.append(away_team_goals_for)
			c_train.append(away_team_goals_against)

		away_team_shots_for = 0
		away_team_shots_against = 0
		matches_counted = 0
		for i in range(max(0,om_index-matches_to_count),om_index):
			if away_team_matches[i][2] == match[1]: #away team at home
				away_team_shots_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][5])
				away_team_shots_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][6])
			else:
				away_team_shots_for += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][6])
				away_team_shots_against += (1/(np.log(max(0.01,matches_counted)) + 1))*int(away_team_matches[i][5])
			matches_counted +=1

		if matches_counted >= max(int(matches_to_count*0.6), 1):
			away_team_shots_for = away_team_shots_for/matches_counted
			away_team_shots_against = away_team_shots_against/matches_counted
			c_train.append(away_team_shots_for)
			c_train.append(away_team_shots_against)

		if len(c_train) == 12:
			inputs.append(c_train)
			targets.append(c_traint)

	return inputs,targets



with open('Stash/testseason/test_home_team_dict.txt','r') as home_dict_file:
	home_team_dict = eval(home_dict_file.read())

with open('Stash/testseason/test_away_team_dict.txt','r') as away_dict_file:
	away_team_dict = eval(away_dict_file.read())

with open('Stash/testseason/test_all_matches.txt','r') as all_matches_file:
	all_matches = eval(all_matches_file.read())

np.random.shuffle(all_matches)

number_of_matches = len(all_matches)

training_matches = all_matches[:int(number_of_matches/2)]
validation_matches = all_matches[int(number_of_matches/2):int(number_of_matches-(number_of_matches/4))]
testing_matches = all_matches[int(number_of_matches-(number_of_matches/4)):number_of_matches]

train, traint = make_sets(training_matches, home_team_dict, away_team_dict)
valid, validt = make_sets(validation_matches, home_team_dict, away_team_dict)
test, testt = make_sets(testing_matches, home_team_dict, away_team_dict)

with open('Stash/testseason/test_train_s.txt','w') as train_file:
	train_file.write(str(train))

with open('Stash/testseason/test_traint_s.txt','w') as traint_file:
	traint_file.write(str(traint))

with open('Stash/testseason/test_valid_s.txt','w') as valid_file:
	valid_file.write(str(valid))

with open('Stash/testseason/test_validt_s.txt','w') as validt_file:
	validt_file.write(str(validt))

with open('Stash/testseason/test_test_s.txt','w') as test_file:
	test_file.write(str(test))

with open('Stash/testseason/test_testt_s.txt','w') as testt_file:
	testt_file.write(str(testt))
