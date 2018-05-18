from flask import Flask, request
import json
import requests
import os

from . import witai_helpers
from . import send_helpers

fb_verify_token = os.environ['VERIFYTOKEN']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_verification():
  """Implements webhook verification as outlined by the Messenger Platform"""

  # Parse query params
  mode = request.args['hub.mode']
  token = request.args['hub.verify_token']
  challenge = request.args['hub.challenge']

  if mode and token:
    if mode == 'subscribe' and token == fb_verify_token:
      print('WEBHOOK VERIFIED...')
      return challenge
    else:
      print('WEBHOOK NOT VERIFIED...')
      return 'not verified', 403

@app.route('/', methods=['POST'])
def handle_webhook_events():
  """
  Primary handler for webhook events. Determines the message intent
  and responds accordingly.
  """

  body = request.get_json()
  if body['object'] == 'page':
    for entry in body['entry']:
    
      if 'messaging' in entry:
        message_text = entry['messaging'][0]['message']['text']
        sender_id = entry['messaging'][0]['sender']['id']
        response = witai_helpers.determine_response(message_text)
        send_helpers.respond_text(sender_id, response)
    
    return 'EVENT RECEIVED...'
  else:
    return 'bad', 404

if __name__ == '__main__':
  app.run()