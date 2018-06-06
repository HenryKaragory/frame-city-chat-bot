import requests
import datetime
import os

# Setup for wit.ai URIs, version string, and the required authentication token.
WIT_API_URL = 'https://api.wit.ai/{path}'
WIT_AI_VERSION = '20180518' # TODO: CHANGE THIS TO A CONSTANT
AIT_AI_TOKEN = os.environ['WITAITOKEN']

# TODO: REMOVE THIS FUNCTION FROM THE APPLICATION, REPLACE WITH API WRAPPER BELOW
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

# TODO: REMOVE THIS FUNCTION FROM THE APPLICATION, REPLACE WITH API WRAPPER BELOW
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

def make_request(token, method, path, params=None):
	"""
	Makes a request to the Witai HTTP api.

	Parameters:
		token - App token
		path - Path to specify resource
		method - The HTTP method to be used, either GET or POST
		params - The parameters for the query string

	Returns:
		Body of response from witai api as JSON.
	"""
	headers = {'Authorization': 'Bearer ' + wit_ai_token}
	params['v'] = WIT_AI_VERSION
	response = requests.request(
		method=method,
		url=WIT_API_URL.format(path=path),
		headers=headers,
		params=params,
	)
	if response.status_code != 200:
		print('There was an error accessing the Witai API')
		return {}
	try:
		return response.json()
	except ValueError:
		print('There was an error in the Witai API reponse!')
		return {}


class WitAIBot:
	__init__(self, token):
		self.token = token

	def get_meaning(self, sentence, n=1, verbose_flag=False):
		params = {'q': sentence, 'n', n, 'verbose': verbose_flag}
		return make_request(self.token, 'GET', '/message', params)

	def get_app_entities(self):
		return make_request(self.token, 'GET', '/entities')


