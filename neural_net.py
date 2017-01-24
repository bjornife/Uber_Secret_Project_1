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

with open('train_s.txt','r') as train_file:
	train = eval(train_file.read())

with open('traint_s.txt','r') as traint_file:
	traint = eval(traint_file.read())

with open('valid_s.txt','r') as valid_file:
	valid = eval(valid_file.read())

with open('validt_s.txt','r') as validt_file:
	validt = eval(validt_file.read())

with open('test_s.txt','r') as test_file:
	test = eval(test_file.read())

with open('testt_s.txt','r') as testt_file:
	testt = eval(testt_file.read())

#INPUT:
#<home team form> <home team home form> <inter-team form> <away team form> <away team away form>
#NEW INPUT
#<home team form> <home team home form> <home team goals for> <home team goals against> <inter-team form> <away team form> <away team away form> <away team goals for> <away team goals against>
#NEWEST INPUT
#<home team form> <home team home form> <home team goals for> <home team goals against> <home team shots for> <home team shots against> <away team form> <away team away form> <away team goals for> <away team goals against> <away team shots for> <away team shots against>

#n = FeedForwardNetwork()
#inLayer = LinearLayer(5)
#hiddenLayer = SigmoidLayer(5)
#outLayer = LinearLayer(3)

#n.addInputModule(inLayer)
#n.addModule(hiddenLayer)
#n.addOutputModule(outLayer)

#in_to_hidden = FullConnection(inLayer, hiddenLayer)
#hidden_to_out = FullConnection(hiddenLayer, outLayer)

#n.addConnection(in_to_hidden)
#n.addConnection(hidden_to_out)

#n.sortModules()

nhidden = 6
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
all_results = []
for i in range(6,7):
	print("HIDDEN NODES: ", str(i))
	n = buildNetwork(np.shape(train)[1], i, np.shape(traint)[1], outclass = SigmoidLayer)

	trainer = BackpropTrainer(n,training_set, momentum = momentum, verbose = True, weightdecay = 0.0, learningrate = 0.2)

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

	total_earnings = 0
	total_random_earnings = 0
	total_naive_earnings = 0
	with open('test_reference.txt') as ref_file:
		reference = eval(ref_file.read())
		for i in range(len(test_results)):
			total_earnings -= 10
			total_random_earnings -=10
			total_naive_earnings -=10
			if np.argmax(testt[i]) == 0:
				try:
					total_naive_earnings += float(reference[i][7])*10
				except ValueError:
					pass
			if test_results[i] == np.argmax(testt[i]):
				try:
					total_earnings += float(reference[i][test_results[i] + 7])*10
				except ValueError:
					pass
					#some odds values are void
			if random.randint(0,2) == np.argmax(testt[i]):
				try:
					total_random_earnings += float(reference[i][test_results[i] + 7])*10
				except ValueError:
					pass
					#some odds values are void
	print("Total earnings: ", total_earnings)
	print("Earnings per game: ", total_earnings/len(testt))
	print("Total random earnings: ", total_random_earnings)
	print("Total random earnings per game: ", total_random_earnings/len(testt))
	print("Total naive earnings: ", total_naive_earnings)
	print("Total naive earnings per game: ", total_naive_earnings/len(testt))

	### Alternatively: Bet only when prediction is away win ###
	total_earnings = 0

	with open('test_reference.txt') as ref_file:
		reference = eval(ref_file.read())
		for i in range(len(test_results)):
			if test_results[i] == 2:
				total_earnings -= 10
				if test_results[i] == np.argmax(testt[i]):
					try:
						total_earnings += float(reference[i][test_results[i] + 7])*10
					except ValueError:
						pass
						#some odds values are void
	print("Total earnings on away bets: ", total_earnings)
	print("Earnings per game on away bets: ", total_earnings/test_results.count(2))

	### Or... when the prediction is a home win ###
	total_earnings = 0

	with open('test_reference.txt') as ref_file:
		reference = eval(ref_file.read())
		for i in range(len(test_results)):
			if test_results[i] == 0:
				total_earnings -= 10
				if test_results[i] == np.argmax(testt[i]):
					try:
						total_earnings += float(reference[i][test_results[i] + 7])*10
					except ValueError:
						pass
						#some odds values are void
	print("Total earnings on home bets: ", total_earnings)
	print("Earnings per game on home bets: ", total_earnings/test_results.count(0))


#with open('results.txt','w') as outputfile:
#	outputfile.write(str(test_results))
#print(n.activate([12,5,10,22,-2,20,15,21,11]))
#print(n.activate([26,15,23,14,3,14,4,9,19]))


"""
****LOG****
For some reason, it seems that classification with linear output yields promising results, whereas classification with sigmoid output does not.
"""