import numpy as np
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

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



training_set = ClassificationDataSet(12, 3)
test_set = ClassificationDataSet(12, 3)

for i in range(np.shape(train)[0]):
	training_set.addSample(train[i],traint[i])

for i in range(np.shape(valid)[0]):
	training_set.addSample(valid[i],validt[i])

for i in range(np.shape(test)[0]):
	test_set.addSample(test[i],testt[i])

training_set._convertToOneOfMany()
test_set._convertToOneOfMany()

fnn = buildNetwork(training_set.indim, 6, training_set.outdim, outclass=SoftmaxLayer)


trainer = BackpropTrainer(fnn, dataset=training_set, momentum=0.1, verbose=True, weightdecay=0.01)

trainer.trainUntilConvergence(verbose = True, maxEpochs = 2)

trainer.testOnData(dataset = test_set, verbose = True)

trnresult = percentError(trainer.testOnClassData(),training_set['class'])
tstresult = percentError(trainer.testOnClassData(dataset=test_set ), test_set['class'])


print("epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult)

