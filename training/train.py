import requests
import os, sys
import datetime

today = datetime.datetime.today()

# Setting up the request to the HTTP API
# The request body contains a JSON array of samples
headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + os.environ['WITAITOKEN'] }
params = {'v': today.strftime('%Y%m%d')}


files_to_process = sys.argv [1:]
files_to_process = map(lambda x: x + '.txt', files_to_process)

for file_name in files_to_process:
	request_body = []
	with open(file_name, 'r') as f:

		# Get the entity, value, and other possible information into a dict
		entity_information = f.readline().rstrip('\n').split(',')
		entities_dict = {}
		for entity_info in entity_information:
			entity_info_list = entity_info.split(':')
			entities_dict[entity_info_list[0].lstrip()] = entity_info_list[1].lstrip()

		print(entities_dict)
		for line in f:
			sample = {}
			sample['text'] = line.rstrip('\n')
			sample['entities'] = [{'entity': entities_dict['entity'], 'value': entities_dict['value']}]
			request_body.append(sample)
			r = requests.post('https://api.wit.ai/samples',
					params = params,
					headers = headers,
					json = request_body
				)
			print(r.status_code)
	print(request_body)

