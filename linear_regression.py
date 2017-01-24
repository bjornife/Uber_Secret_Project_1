import numpy as np
from scipy import stats
from sklearn import linear_model

with open('train_s.txt','r') as train_file:
	train = np.array(eval(train_file.read()), dtype = float)

with open('traint_s.txt','r') as traint_file:
	traint = np.array(eval(traint_file.read()), dtype = float)


regger = linear_model.LinearRegression(fit_intercept = True, normalize = True)

regger.fit(train, traint)

print(regger.coef_)

#slope, intercept, r_value, p_value, std_err = stats.linregress(train,traint)