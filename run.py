import os
from make_sets import sets_maker
from neural_net import neural_net

sets = sets_maker()
train,traint,valid,validt,test,testt,reference = sets.run()
nn = neural_net()
nn.run(train,traint,valid,validt,test,testt,reference)
