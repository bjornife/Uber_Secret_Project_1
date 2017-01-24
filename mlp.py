''' Feel free to use numpy for matrix multiplication and
	other neat features.
	You can write some helper functions to
	place some calculations outside the other functions
	if you like to.

	This pre-code is a nice starting point, but you can
	change it to fit your needs.
'''
import numpy as np
import random

class mlp:
	def __init__(self, ninput, noutput, nhidden):
		self.beta = 1
		self.eta = 0.1 #learning rate
		self.momentum = 0.0 #Maybe explore this

		self.input_to_hidden = np.random.rand(ninput+1,nhidden)*4-2
		self.hidden_to_output = np.random.rand(nhidden+1,noutput)*4-2

	def earlystopping(self, inputs, targets, valid, validtargets):
		previous_validation_error = float('inf')
		uphills = 0

		while(uphills < 1):
			self.train(inputs, targets)

			errors = self.validate(valid, validtargets)
			current_validation_error = np.sum(errors)
			print("validation error: 			", current_validation_error)
			print("previous validation error:		", previous_validation_error)
			if(current_validation_error >= previous_validation_error):
				previous_validation_error = current_validation_error
				#uphills+=1
				break

			previous_validation_error = current_validation_error
			uphills = 0
			#average error

			#validate
			#if validation error increases: stop.
		with open('ithw.txt','w') as ithwf:
			for item in self.input_to_hidden:
				for it in item:	
					ithwf.write(str(it))
					ithwf.write(' ')
				ithwf.write(';')
			
		with open('htow.txt','w') as htowf:
			for item in self.hidden_to_output:
				for it in item:
					htowf.write(str(it))
					htowf.write(' ')					
				htowf.write(';')

		#confusion

	def train(self, inputs, targets, iterations=100):
		#SUM TING WONG:
		#The validation error does not decrease.

		#delta_ith = np.zeros((np.shape(inputs)[0], np.shape(self.input_to_hidden)[1]+1))
		#delta_hto = np.zeros((np.shape(inputs)[0], np.shape(targets)[1]))
		delta_hto = np.zeros((np.shape(self.hidden_to_output)))
		delta_ith = np.zeros((np.shape(self.input_to_hidden)))


		for i in range(iterations):
			activations = self.forward(inputs)
			outputs = activations[0]
			hidden_activations = np.hstack((activations[1], np.ones((np.shape(activations[1])[0],1))))
			
			#FOR REGRESSION
			#output_errors = (targets-outputs)*outputs
			#hidden_errors = hidden_activations*(np.dot(output_errors,np.transpose(self.hidden_to_output)))
			
			#FOR SIGMOID			
			output_errors = (targets-outputs)*outputs*(1.0-outputs)
			hidden_errors = hidden_activations*(1.0-hidden_activations)*(np.dot(output_errors,np.transpose(self.hidden_to_output)))

			
			delta_ith = self.eta*(np.dot(np.transpose(inputs),hidden_errors[:,:-1]))
			delta_ith += delta_ith*self.momentum
			delta_hto = self.eta*(np.dot(np.transpose(hidden_activations),output_errors))
			delta_hto += delta_hto*self.momentum
			##TODO: make dimensions match

			delta_ith = np.vstack((delta_ith,np.zeros((1,np.shape(delta_ith)[1]))))
			
			self.input_to_hidden += delta_ith*self.momentum
			self.hidden_to_output += delta_hto*self.momentum

		""" FOR CLASSIFICATION """
		t = 0
		f = 0
		for i in range(np.shape(targets)[0]):
			if np.argmax(outputs[i]) == np.argmax(targets[i]):
				t+=1
			else:
				f+=1
		print("TRAINING SET CORRECTNESS:		", t/(t+f)*100, "%")
		

	def validate(self, valid, validtargets):
		activations = self.forward(valid)
		outputs = activations[0]
		hidden_activations = activations[1]

		
		t = 0
		f = 0
		for i in range(np.shape(validtargets)[0]):
			if np.argmax(outputs[i]) == np.argmax(validtargets[i]):
				t+=1
			else:
				f+=1
		
		print("VALIDATION SET CORRECTNESS:		", t/(t+f)*100, "%") 	
		
		
		return np.exp2(validtargets-outputs) #output errors


	def forward(self, inputs):
		#print("BEFORE CALL: ", self.input_to_hidden)
		hidden_activations = self.calculate_activations(inputs, self.input_to_hidden) #Nx8 matrix?
		output_activations = self.calculate_activations(hidden_activations, self.hidden_to_output)
		
		return output_activations, hidden_activations

	def confusion(self, inputs, targets):
		confusion_matrix = np.zeros((np.shape(targets)[1],np.shape(targets)[1]))
		outputs = self.forward(inputs)[0]
		

		"""FOR REGRESSION
		correct = 0
		total_error = 0
		for i in range(np.shape(targets)[0]):
			if targets[i][0] > 0 and outputs[i][0] > 0 or targets[i][0] <= 0 and outputs[i][0] <= 0:
				correct += 1
			total_error += np.sqrt((targets[i][0] - outputs[i][0])**2)

		avg_error = total_error/np.shape(targets)[0]
		"""
		correct = 0
		
		for i in range(np.shape(targets)[0]):
			answer = np.argmax(outputs[i])
			target = np.argmax(targets[i])
			confusion_matrix[target][answer] +=1
			correct = correct+1 if target == answer else correct
			
			#if answer == target:
			#	confusion_matrix[answer][answer] +=1
			#else:
			#	confusion_matrix[answer][target]
		
		print(confusion_matrix)
		print("TESTING SET CORRECTNESS:		", (correct/np.shape(targets)[0])*100, "%")
			

		print("TESTING SET CORRECTNESS:		", (correct/np.shape(targets)[0])*100, "%")
		#print("AVERAGE ERROR:				", avg_error)
		#for j in range(100):
		#	print(outputs[j], " - ", targets[j])
		return correct/np.shape(targets)[0]#,total_error

	def calculate_activations(self, inputs, weights):

		inputs_and_bias = np.hstack((inputs, np.ones((np.shape(inputs)[0],1)))) #weights are NaN
		activations = np.dot(inputs_and_bias,weights)
		
		vectorized_sigmoid = np.vectorize(self.sigmoid_function)
		activations = vectorized_sigmoid(activations)
		#activations = self.activation_function(activations)
		
		
		return activations

	def sigmoid_function(self, x):
		#TODO: implement 4.12?
		return 1/(1+np.exp(-self.beta*x))

	#4.12, no idea if it works.
	def activation_function(self, activations):
		return np.exp(activations)/np.sum(np.exp(activations))