import requests 
import os

# Setup for facebook messenger send API uris
send_message_uri = 'https://graph.facebook.com/v2.6/me/messages'

PAT = os.environ['PAT']

def respond_text(recipient_id, text_message):
  """Respond to a user message with text_message"""
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'messaging_type': 'RESPONSE',
    'recipient': {'id': recipient_id}, 
    'message': {'text': text_message}
    }
  r = requests.post(send_message_uri,
      headers=headers,
      params=params,
      json=body
    )

def respond_typing(recipient_id, typing_on):
  """Show the typing symbol in the chatbox."""
  action = 'typing_on' if (typing_on) else 'typing_off'
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'recipient': {'id': recipient_id}, 
    'sender_action': {action}
    }
  send_message(recipient_id, params, header, body)

def respond_mark_seen(recipient_id):
  """Mark a message sent by a user as seen."""

  action = 'mark_seen'
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'recipient': {'id': recipient_id}, 
    'sender_action': {action}
    }
  send_message(recipient_id, params, header, body)

def send_message(recipient_id, params, header, body):
  return requests.post(send_message_uri,
      headers=headers,
      params=params,
      json=body
    )