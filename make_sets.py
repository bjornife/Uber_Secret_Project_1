import os
from operator import itemgetter
import re
import numpy as np
import mlp
from datetime import date

#idea: add fatigue rating based on recency of latest matches.
#idea: center the data by subtracting the mean
#also, make this a class and avoid writing to file

class sets_maker(object):

	def run(self):

		with open('home_team_dict.txt','r') as home_dict_file:
			home_team_dict = eval(home_dict_file.read())

		with open('away_team_dict.txt','r') as away_dict_file:
			away_team_dict = eval(away_dict_file.read())

		with open('all_matches.txt','r') as all_matches_file:
			all_matches = eval(all_matches_file.read())

		np.random.shuffle(all_matches)

		number_of_matches = len(all_matches)

		testing_matches = []
		testing_match_reference = []

		i=0
		matches_in_test_set = 0
		while matches_in_test_set < int(number_of_matches/4) and i < len(all_matches):
			if len(all_matches[i]) > 7:
				testing_matches.append(all_matches[i])
				testing_match_reference.append(all_matches[i])
				matches_in_test_set+=1
				del all_matches[i]
			i+=1

		number_of_matches = len(all_matches) #needs to be redefined due to changing size

		training_matches = all_matches[:int(number_of_matches - (number_of_matches/4))]
		validation_matches = all_matches[int(number_of_matches-(number_of_matches/4)):number_of_matches]

		#training_matches = all_matches[:int(number_of_matches/2)]
		#validation_matches = all_matches[int(number_of_matches/2):int(number_of_matches-(number_of_matches/4))]
		#testing_matches = all_matches[int(number_of_matches-(number_of_matches/4)):number_of_matches]

		train, traint = self.make_sets(training_matches, home_team_dict, away_team_dict, data_type = 'TRAINING')
		valid, validt = self.make_sets(validation_matches, home_team_dict, away_team_dict, data_type = 'VALIDATION')
		test, testt = self.make_sets(testing_matches, home_team_dict, away_team_dict, data_type = 'TESTING')
		
		return train,traint,valid,validt,test,testt,testing_match_reference

		"""
		with open('train_s.txt','w') as train_file:
			train_file.write(str(train))

		with open('traint_s.txt','w') as traint_file:
			traint_file.write(str(traint))

		with open('valid_s.txt','w') as valid_file:
			valid_file.write(str(valid))

		with open('validt_s.txt','w') as validt_file:
			validt_file.write(str(validt))

		with open('test_s.txt','w') as test_file:
			test_file.write(str(test))

		with open('testt_s.txt','w') as testt_file:
			testt_file.write(str(testt))

		with open('test_reference.txt','w') as ref_file:
			ref_file.write(str(testing_match_reference))
		"""
	def get_date_diff(self,datestring1, datestring2):
		datestring1 = str(datestring1)
		year1 = datestring1[:4]
		month1 = datestring1[4:6]
		day1 = datestring1[6:]
		if day1[0] == '0':
			day1 = day1[1:]

		datestring2 = str(datestring2)
		year2 = datestring2[:4]
		month2 = datestring2[4:6]
		day2 = datestring2[6:]
		if day2[0] == '0':
			day2 = day2[1:]

		#look away!	
		return int(str(date(int(year1), int(month1), int(day1)) - date(int(year2),int(month2),int(day2))).split()[0])


	def make_sets(self,matches, home_team_dict, away_team_dict, test_written = False, data_type = 'DATA'):
		inputs = []
		targets = []
		
		matches_to_count = 50
		matches_covered = 0
		number_of_matches = len(matches)
		percent_done = 0
		for match in matches:

			matches_covered +=1
			if matches_covered == int(number_of_matches/10):
				percent_done +=10
				print(data_type, percent_done, "% READY")
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

			"""
			if not test_written:
				with open('trouble/home_team_home_matches.txt','w') as f1, open('trouble/home_team_away_matches.txt','w') as f2, open('trouble/away_team_home_matches.txt','w') as f3, open('trouble/away_team_away_matches.txt', 'w') as f4, open('trouble/home_team_matches.txt', 'w') as f5, open('trouble/away_team_matches.txt','w') as f6:
					f1.write(str(home_team_home_matches))
					f2.write(str(home_team_away_matches))
					f3.write(str(away_team_home_matches))
					f4.write(str(away_team_away_matches))
					f5.write(str(home_team_matches))
					f6.write(str(away_team_matches))
					test_written = True
			"""
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
			home_team_exhaustion = 0
			matches_counted = 0
			for i in range(max(0,ht_index-matches_to_count),ht_index):
				if i < (ht_index-matches_to_count) + 2:
					home_team_exhaustion += (1/int(self.get_date_diff(match[0], home_team_matches[i][0])))

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

			"""
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
			"""
			c_train.append(home_team_exhaustion)

			#TODO: Implement intra-team form?

			away_team_form = 0
			away_team_exhaustion = 0
			matches_counted = 0
			for i in range(max(0,om_index-matches_to_count),om_index):
				if i < (om_index-matches_to_count) + 2:
					away_team_exhaustion += (1/int(self.get_date_diff(match[0],away_team_matches[i][0])))

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


			"""
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
			"""
			c_train.append(away_team_exhaustion)

			if len(c_train) == 10:
				inputs.append(c_train)
				targets.append(c_traint)

		#center the data
		inputs = np.asarray(inputs)
		inputs = inputs - inputs.mean(axis=1)[:, np.newaxis]

		return inputs,targets
