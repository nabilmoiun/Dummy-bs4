from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
all_medicine = []
for i in range(5):
	url = "https://medex.com.bd/brands?page={page}".format(page=i)
	page = urlopen(url).read()
	content = bs(page, "html.parser")
	links = [link.get('href') for link in content.find_all('a', {"class": "hoverable-block"})]
	for link in links:
		try:
			medicine_url = urlopen(link).read()
			medicine_details = bs(medicine_url,"html.parser")
			medicine_prop = medicine_details.find_all("div", {"class":"col-xs-12 ac-body"})
			indication = re.sub('<[^>]*>', '', str(medicine_prop[0]))
			therapeutic_class = re.sub('<[^>]*>', '', str(medicine_prop[1]))
			pharmacology = re.sub('<[^>]*>', '', str(medicine_prop[2]))
			dosage_and_administration = re.sub('<[^>]*>', '', str(medicine_prop[3]))
			interaction = re.sub('<[^>]*>', '', str(medicine_prop[4]))
			contradiction = re.sub('<[^>]*>', '', str(medicine_prop[5]))
			side_effects = re.sub('<[^>]*>', '', str(medicine_prop[6]))
			pregnancy_and_limitation = re.sub('<[^>]*>', '', str(medicine_prop[7]))
			precaution = re.sub('<[^>]*>', '', str(medicine_prop[8]))
			storage = re.sub('<[^>]*>', '', str(medicine_prop[9]))
			all_medicine.append([indication, therapeutic_class, pharmacology,
			dosage_and_administration, interaction, contradiction, side_effects,
			pregnancy_and_limitation, precaution, storage])
		except IndexError:
			pass
# for f in all_medicine[28]:
# 	try:
# 		print(f)
# 	except UnicodeEncodeError:
# 		pass
print(len(all_medicine))