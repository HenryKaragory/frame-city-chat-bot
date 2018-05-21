import requests 
import os

from . import witai_helpers

# Setup for facebook messenger send API uris
send_message_uri = 'https://graph.facebook.com/v2.6/me/messages'

PAT = os.environ['PAT']

def send_response(sender_id, message):
  """
  This function sends a response to the user identified by sender_id.

  Parameters:
    sender_id: The psid of the user that sent the message.
    message: The message sent by the user identified by psid.
  """
  response = ''

  if message == 'information':
    send_information_buttons(sender_id)

  meaning = witai_helpers.determine_meaning(message)

  if meaning == 'general_price_information' or meaning == 'general_price_info':
    response = 'We have the cheapest prices!'
  elif meaning == 'operation_hours':
    response = 'We are open M-Sat from 9am to 6pm.'
  elif meaning == 'general_location_information':
    reponse = "We are located on High Street right behind Tj's Country Place!"
  elif meaning == 'general_service_information':
    response = 'We offer custom framing at affordable prices!'
  elif meaning == 'general_quality_information':
    response = 'We are the best framers in central Ohio!'
  elif meaning == 'rude_customer':
    response = 'That was rude!'

  send_text_response(sender_id, response)

def send_message(recipient_id, params, headers, body):
  return requests.post(send_message_uri,
      headers=headers,
      params=params,
      json=body
    )

def send_text_response(recipient_id, text_message):
  """Respond to a user message with text_message"""
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'messaging_type': 'RESPONSE',
    'recipient': {'id': recipient_id}, 
    'message': {'text': text_message}
    }
  send_message(recipient_id, params, headers, body)

def send_typing(recipient_id, typing_on):
  """Show the typing symbol in the chatbox."""
  action = 'typing_on' if (typing_on) else 'typing_off'
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'recipient': {'id': recipient_id}, 
    'sender_action': {action}
    }
  send_message(recipient_id, params, header, body)

def send_mark_seen(recipient_id):
  """Mark a message sent by a user as seen."""

  action = 'mark_seen'
  params = {'access_token': PAT}
  headers = {'Content-type': 'application/json'}
  body = {
    'recipient': {'id': recipient_id}, 
    'sender_action': {action}
    }
  send_message(recipient_id, params, header, body)

def send_information_buttons(recipient_id):
  """
  This function sends a text message with three buttons to
  help the user learn how to use the bot.
  
  TODO: DETERMINE WHAT THE THREE BUTTONS ARE AND FINISH CODING THEM

  Parameters:
    recipient_id: The psid for the recipient of the message.
  """
  headers = {'Content-type': 'application/json'}
  params = {'access_token': PAT}
  body = {
    "recipient":{"id": recipient_id},
    "message":{
      "attachment":{
        "type":"template",
        "payload":{
          "template_type":"button",
          "text":"What do you want to do next?",
          "buttons":[
            {
              "type": "postback",
              "title": "Postback button test",
              "payload": "test_payload"
            }
          ]
        }
      }
    }
  }
  send_message(recipient_id, params, headers, body)


def handle_postback(sender_id, payload):
  """
  This function is the main handler for postback events sent to the webhook.
  """
  if payload == 'test_payload':
    send_text_response(sender_id, 'The test postback button worked!')

