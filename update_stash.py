import urllib.request
import re
import os, shutil
import zipfile

def fetch_data(number_of_years = 24):


	folder = '../../Football_Data/Zipstash'
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)
		
	folder = '../../Football_Data/Stash'
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)

	response = 	urllib.request.urlopen('http://www.football-data.co.uk/downloadm.php')

	url_string = str(response.read())

	match = re.search('<P><B>CSV</B>.*?</table>',url_string)

	if not match:
		print("ERROR IN FETCHING DATA")
		return

	full_table = match.group(0)
	links = re.finditer('mmz.*?\.zip',full_table)

	files = []
	i = 0
	for item in links:
		link = 'http://www.football-data.co.uk/' + item.group(0)
		print("Downloading ", link)
		filename = '../../Football_Data/Zipstash/data_' + str(i) + '.zip'
		response = urllib.request.urlretrieve(link, filename = filename)
		i+=1
		

	i = 0
	for file in os.listdir('../../Football_Data/Zipstash'):
		file_path = os.path.join('../../Football_Data/Zipstash', file)
		print('unzipping ', file_path)
		zipped_file = zipfile.ZipFile(file_path,'r')
		zipped_file.extractall('../../Football_Data/Stash')
		zipped_file.close()
		for datafile in os.listdir('../../Football_Data/Stash'):
			trimmed_name = os.path.splitext(datafile)[0]
			datafile_path = '../../Football_Data/Stash/' +  datafile
			os.rename(datafile_path, '../../Football_Data/Stash/' + trimmed_name + str(i) + '.csv')
		i+=1
	#with open('test_download_file.zip','w') as outfile:
	#	outfile.write(files[0])

fetch_data()
#download files

#remove files in stash

#extract zip files to stash