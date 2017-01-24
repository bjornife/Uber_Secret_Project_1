import urllib.request
import re

def fetch_data():
		
	response = 	urllib.request.urlopen('http://www.football-data.co.uk/downloadm.php')

	url_string = str(response.read())

	match = re.search('<P><B>CSV</B>.*?</table>',url_string)

	if not match:
		print("ERROR IN FETCHING DATA")
		return

	full_table = match.group(0)
	links = re.finditer('mmz.*?\.zip',full_table)

	for item in links:
		print(item.group(0))
fetch_data()
#download files

#remove files in stash

#extract zip files to stash