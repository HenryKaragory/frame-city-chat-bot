import requests
import datetime
import os

# Setup for wit.ai URIs, version string, and the required authentication token.
wit_ai_message_meaning_uri = 'https://api.wit.ai/message'
wit_ai_version = datetime.datetime.today().strftime('%Y%m%d')
wit_ai_token = os.environ['WITAITOKEN']

def determine_meaning(message):
	"""
	This function determines the most likely intent entity value according to the wit.ai application.

	Parameters:
		message - The message that witai will determine the entity and value for
	"""

	meaning_entities_dict = get_meaning_entities(message)

	# List to store custom user intents
	intent_value_list = []

	if 'intent' in meaning_entities_dict:
		intent_value_list = list(map(lambda x: x['value'], meaning_entities_dict['intent']))


	return ('undetermined' if (len(intent_value_list)==0) else intent_value_list[0])

def get_meaning_entities(message):
	"""
	This function returns the dictionary of entities returned by wit.ai according
	to the message that was sent. The string message must be less than 256 characters
	in lest and may not be empty.
	"""

	headers = {'Authorization': 'Bearer ' + wit_ai_token}
	params = {'v': wit_ai_version, 'q': message, 'n': 8}
	r = requests.get(wit_ai_message_meaning_uri,
			headers=headers,
			params=params
		)
	body = r.json()
	return body['entities']
