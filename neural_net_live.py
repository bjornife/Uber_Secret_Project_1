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

with open('live_s.txt','r') as test_file:
	test = eval(test_file.read())


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

#for i in range(np.shape(test)[0]):
#	training_set.addSample(test[i],testt[i])

testing_set = SupervisedDataSet(np.shape(test)[1], 3)
for i in range(len(test)):
	testing_set.addSample(test[i],[0,0,0])

momentum = 0.04
all_results = []
	

n = buildNetwork(np.shape(train)[1], nhidden, np.shape(traint)[1], outclass = SigmoidLayer)

trainer = BackpropTrainer(n,training_set, momentum = momentum, verbose = True, weightdecay = 0.0, learningrate = 0.2)

trainer.trainUntilConvergence(verbose = True, maxEpochs = 10)

test_results = trainer.testOnClassData(dataset = testing_set, verbose = True)

with open('final_results.txt','w') as outputfile:
	outputfile.write(str(test_results))