from flask import Flask, request
import json
import requests
import os

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = ''

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_verification():
  verify_token = os.environ['VERIFYTOKEN']

  # Parse query params
  mode = request.args['hub.mode']
  token = request.args['hub.verify_token']
  challenge = request.args['hub.challenge']

  if mode and token:
    if mode == 'subscribe' and token == verify_token:
      print('WEBHOOK VERIFIED...')
      return challenge
    else:
      print('WEBHOOK NOT VERIFIED...')
      return 'not verified', 403

@app.route('/', methods=['POST'])
def handle_messages():
  body = request.get_json()
  print(type(body))
  print(body)

  if body['object'] == 'page':
    for entry in body['entry']:
      webhook_event = entry['messaging'][0]['message']
      print(webhook_event)
    return 'EVENT RECEIVED...'
  else:
    return 'bad', 404

def respond():
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'messaging_type': 'RESPONSE',
    'recipient': {'id': recipient}, 
    'message': {'text': 'Hello!'}
    }
  r = requests.post('https://graph.facebook.com/v2.6/me/messages')


if __name__ == '__main__':
  app.run()