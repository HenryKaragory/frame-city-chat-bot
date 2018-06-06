from flask import Flask, request
from db import schema, session
from . import send_helpers

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import json
import atexit
import requests
import os

# Set up jobs to run in the background
scheduler = BackgroundScheduler()
scheduler.add_job(
  func=send_request_for_review, 
  trigger=IntervalTrigger(hours=72),
  id='request_review_job',
  name='Requests reviews from customers every three days.')
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_verification():
  """Implements webhook verification as outlined by the Messenger Platform"""
  fb_verify_token = os.environ['VERIFYTOKEN']

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
  print(body)
  if body['object'] == 'page':
    for entry in body['entry']:
      
      if 'postback' in entry['messaging'][0]:
        sender_id = entry['messaging'][0]['sender']['id']
        payload = entry['messaging'][0]['postback']['payload']
        with session_scope() as session:
          send_helpers.handle_postback(sender_id, payload, session)
      elif 'message' in entry['messaging'][0]:
        message_text = entry['messaging'][0]['message']['text']
        sender_id = entry['messaging'][0]['sender']['id']
        with session_scope() as session:
          send_helpers.send_response(sender_id, message_text, session)

    return 'EVENT RECEIVED...'
  else:
    return 'bad', 404

if __name__ == '__main__':
  app.run()