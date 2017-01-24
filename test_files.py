import os
from operator import itemgetter
import re
import numpy as np
import mlp



all_matches = []

for filename in os.listdir('Stash'):
	file = open('Stash/' + filename,'r')
	season = file.read().rstrip().split('\n')
	all_matches.extend(season)
	file.close()
i=0

count = 0
tcount = 0
while i < len(all_matches):
	if ",HS," in all_matches[i]:
		print(all_matches[i])
		count+=1
	if ",HST," in all_matches[i]:
		tcount+=1
	i+=1


print(count, tcount)