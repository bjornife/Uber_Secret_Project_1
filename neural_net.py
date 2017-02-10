import numpy as np
import random
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import percentError
from pybrain.tools.neuralnets import NNregression

#INPUT:
#<home team form> <home team home form> <inter-team form> <away team form> <away team away form>
#NEW INPUT
#<home team form> <home team home form> <home team goals for> <home team goals against> <inter-team form> <away team form> <away team away form> <away team goals for> <away team goals against>
#NEWEST INPUT
#<home team form> <home team home form> <home team goals for> <home team goals against> <home team shots for> <home team shots against> <away team form> <away team away form> <away team goals for> <away team goals against> <away team shots for> <away team shots against>

class neural_net(object):

	def run(self,train,traint,valid,validt,test,testt,reference):
		nhidden = 7
		nhidden2 = 4
		nhidden3 = 6

		training_set = SupervisedDataSet(np.shape(train)[1], np.shape(traint)[1])
		#training_set = ClassificationDataSet(np.shape(traint)[1])

		for i in range(np.shape(train)[0]):
			training_set.addSample(train[i],traint[i])

		validation_set = SupervisedDataSet(np.shape(valid)[1], np.shape(validt)[1])

		for i in range(np.shape(valid)[0]):
			training_set.addSample(valid[i],validt[i])

		testing_set = SupervisedDataSet(np.shape(test)[1], np.shape(testt)[1])

		#for i in range(np.shape(test)[0]):
		#	training_set.addSample(test[i],testt[i])

		testing_set = SupervisedDataSet(np.shape(test)[1], np.shape(testt)[1])
		for i in range(len(test)):
			testing_set.addSample(test[i],testt[i])

		momentum = 0.04
		learningrate = 0.1
		all_results = []
			
		for k in range(1):
			n = buildNetwork(np.shape(train)[1], nhidden, np.shape(traint)[1], outclass = SigmoidLayer)

			trainer = BackpropTrainer(n,training_set, momentum = momentum, verbose = True, weightdecay = 0, learningrate = 0.1)

			trainer.trainUntilConvergence(verbose = True, maxEpochs = 10)

			test_results = trainer.testOnClassData(dataset = testing_set, verbose = True)

			away_matches_won = 0
			home_matches_won = 0
			for match in testt:
				if match[0] == 1:
					home_matches_won+=1
				elif match[2] == 1:
					away_matches_won+=1

			print("test set size: ", len(testt))
			print("P_h = ", home_matches_won/len(testt))
			print("P_a = ", away_matches_won/len(testt))

			correct_guesses = 0
			correct_away_guesses = 0
			away_guesses = 0
			correct_home_guesses = 0
			home_guesses = 0
			for j in range(len(testt)):
				if test_results[j] == np.argmax(testt[j]):
					correct_guesses+=1
					if test_results[j] == 2:
						correct_away_guesses+=1
					if test_results[j] == 0:
						correct_home_guesses+=1
				if test_results[j] == 2:
					away_guesses+=1
				if test_results[j] == 0:
					home_guesses+=1

			all_results.append(correct_guesses/len(testt))
			print("Correct = ", correct_guesses/len(testt))
			if away_guesses > 0:
				print("Correct away = ", correct_away_guesses/away_guesses)
			if home_guesses > 0:
				print("Correct home = ", correct_home_guesses/home_guesses)


				""""""""" AND NOW THE BETS! """"""""""""
				"""""""""""""""""""""""""""""""""""""""

			reg_results = []
			for i in range(len(test)):
				reg_results.append(n.activate(test[i]))
				for j in range(3):
					reg_results[i][j] = float(reg_results[i][j])

			bet_index = 5
			total_earnings = 0
			total_random_earnings = 0
			total_naive_earnings = 0
			total_smart_earnings = 0 #only bet where odds are better
			no_smart_bets = 0
			bet_size = 10
			for i in range(len(test_results)):
				total_earnings -= bet_size
				total_random_earnings -= bet_size
				total_naive_earnings -= bet_size
				for j in range(3):
					try:
						if float(reference[i][j+bet_index]) > reg_results[i][j]:
							total_smart_earnings-=10
							no_smart_bets+=1
							if np.argmax(testt[i]) == np.argmax(reg_results[i]):
								total_smart_earnings += float(reference[i][j+bet_index])*bet_size
					except ValueError:
						pass	
				if np.argmax(testt[i]) == 0:
					try:
						total_naive_earnings += float(reference[i][bet_index])*bet_size
					except ValueError:
						pass
				if test_results[i] == np.argmax(testt[i]):
					try:
						total_earnings += float(reference[i][test_results[i] + bet_index])*bet_size
					except ValueError:
						pass
						#some odds values are void
				if random.randint(0,2) == np.argmax(testt[i]):
					try:
						total_random_earnings += float(reference[i][test_results[i] + bet_index])*bet_size
					except ValueError:
						pass
						#some odds values are void
		print("Total earnings: ", total_earnings)
		print("Earnings per game: ", total_earnings/len(testt))
		print("Total random earnings: ", total_random_earnings)
		print("Total random earnings per game: ", total_random_earnings/len(testt))
		print("Total naive earnings: ", total_naive_earnings)
		print("Total naive earnings per game: ", total_naive_earnings/len(testt))
		print("Total smart earnings: ", total_smart_earnings)
		print("Total smart earnings per bet: ", total_smart_earnings/no_smart_bets)
			### Alternatively: Bet only when prediction is away win ###
		total_earnings = 0

		for i in range(len(test_results)):
				if test_results[i] == 2:
					total_earnings -= bet_size
					if test_results[i] == np.argmax(testt[i]):
						try:
							total_earnings += float(reference[i][test_results[i] + bet_index])*bet_size
						except ValueError:
							pass
							#some odds values are void
		print("Total earnings on away bets: ", total_earnings)
		if test_results.count(2) > 0:
			print("Earnings per game on away bets: ", total_earnings/test_results.count(2))

			### Or... when the prediction is a home win ###
		total_earnings = 0

		for i in range(len(test_results)):
			if test_results[i] == 0:
				total_earnings -= bet_size
				if test_results[i] == np.argmax(testt[i]):
					try:
						total_earnings += float(reference[i][test_results[i] + bet_index])*bet_size
					except ValueError:
						pass
							#some odds values are void
		print("Total earnings on home bets: ", total_earnings)
		if test_results.count(0) > 0:
			print("Earnings per game on home bets: ", total_earnings/test_results.count(0))
