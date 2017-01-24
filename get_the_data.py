import os
from operator import itemgetter
import re
import numpy as np
import mlp

accuracy = np.zeros(1)
nhidden = 12


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

	# Train the network
	
net = mlp.mlp(12,3,nhidden)
net.earlystopping(train, traint, valid, validt)
accuracy[0] = net.confusion(test,testt)

print("AVERAGE ACCURACY:			", sum(accuracy)/1)
print("MAX ACCURACY:			", np.argmax(accuracy),":	", accuracy[np.argmax(accuracy)])
print("MIN ACCURACY:			", np.argmin(accuracy),":	", accuracy[np.argmin(accuracy)])