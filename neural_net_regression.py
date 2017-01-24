import numpy as np
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
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

nhidden = 11
nhidden2 = 4
nhidden3 = 6

training_set = SupervisedDataSet(np.shape(train)[1], np.shape(traint)[1])

for i in range(np.shape(train)[0]):
	training_set.addSample(train[i],traint[i])

validation_set = SupervisedDataSet(np.shape(valid)[1], np.shape(validt)[1])

for i in range(np.shape(valid)[0]):
	training_set.addSample(valid[i],validt[i])

testing_set = SupervisedDataSet(np.shape(test)[1], np.shape(testt)[1])

for i in range(np.shape(test)[0]):
	training_set.addSample(test[i],testt[i])




#due to a typo in the library source code, the <eponic> parameter is replaced by <epoinc>
#n = NNregression(training_set, hidden = nhidden, TDS = testing_set, VDS = validation_set, epoinc = 2)
n = NNregression(training_set, hidden = nhidden, epoinc = 1)

#Input values must be normalized in order for regression to work...
n.setupNN()

#A wild error appears: when specifying TDS and VDS, an error reads that output.shape != target.shape
#can probably be solved by saving targets as scalars.
n.runTraining(verbose = True)

n.saveNetwork('pynet.txt')