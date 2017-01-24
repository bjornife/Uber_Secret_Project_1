import os

for i in range(1):
	os.system('python update_stash.py')
	os.system('python make_files_2.py')
	os.system('python make_sets.py')
	os.system('python neural_net.py')