import os

for i in range(1):
	os.system('python update_stash.py')
	os.system('python make_files_live.py')
	os.system('python make_sets_live.py')
	os.system('python neural_net_live.py')