import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
BOT_OAUTH_TOKEN = os.getenv('BOT_OAUTH_TOKEN')
POST_MESSAGE_URL = os.getenv('POST_MESSAGE_URL')
SEARCH_MESSAGE_URL = os.getenv('SEARCH_MESSAGE_URL')
REACTION_URL = os.getenv('REACTION_URL')
REACTION_REMOVE_URL = os.getenv('REACTION_REMOVE_URL')
UPDATE_URL = os.getenv('UPDATE_URL')
CHANNEL_ID = os.getenv('CHANNEL_ID')

def post_message(channel_id, message, thread_ts=None, emoji=None):
  payload = {
    "channel": channel_id,
    "text": message
  }

  if thread_ts:
    payload['thread_ts'] = thread_ts

  headers = {
    "Authorization": "Bearer " + BOT_OAUTH_TOKEN,
    "Content-type": "application/json;charset=UTF-8"
  }
  
  resp = requests.post(POST_MESSAGE_URL, json=payload, headers=headers)

  resp_json = json.loads(resp.text)
  print(resp_json)

  if emoji:
    reaction(channel_id, emoji, resp_json['ts'])

def find_messages(channel_id, text):
  payload = {
    "channel": channel_id
  }

  params = {
    "query": "\"" + text + "\"",
    "sort": "timestamp",
    "sort_dir": "desc"
  }

  headers = {
    "Authorization": "Bearer " + OAUTH_TOKEN,
    "Content-type": "application/json;charset=UTF-8"
  }
  
  resp = requests.get(SEARCH_MESSAGE_URL, params=params, json=payload, headers=headers)

  resp_json = json.loads(resp.text)
  print(resp_json)

def reaction(channel_id, emoji, ts):
  payload = {
    "channel": channel_id,
    "timestamp": ts,
    "name": emoji
  }

  headers = {
    "Authorization": "Bearer " + BOT_OAUTH_TOKEN,
    "Content-type": "application/json;charset=UTF-8"
  }
  
  resp = requests.post(REACTION_URL, json=payload, headers=headers)

def remove_reaction(channel_id, emoji, ts):
  payload = {
    "channel": channel_id,
    "timestamp": ts,
    "name": emoji
  }

  headers = {
    "Authorization": "Bearer " + BOT_OAUTH_TOKEN,
    "Content-type": "application/json;charset=UTF-8"
  }
  
  resp = requests.post(REACTION_REMOVE_URL, json=payload, headers=headers)

def edit_message(channel_id, message, ts, emoji):
  payload = {
    "channel": channel_id,
    "ts": ts,
    "text": message
  }

  headers = {
    "Authorization": "Bearer " + BOT_OAUTH_TOKEN,
    "Content-type": "application/json;charset=UTF-8"
  }
  
  resp = requests.post(UPDATE_URL, json=payload, headers=headers)

  if emoji:
    reaction(channel_id, emoji, ts)

# post_message(CHANNEL_ID, "Test a message", None, 'call_me_hand')
# reaction(CHANNEL_ID, 'tada', '1605086375.000900')
# find_messages(CHANNEL_ID, "Test a message")
# post_message(CHANNEL_ID, "Reply to message", '1605086946.001900', 'tada')
# edit_message(CHANNEL_ID, "Reply to message. This message has been edited", '1605089273.002500', 'call_me_hand')
# remove_reaction(CHANNEL_ID, 'call_me_hand', '1605089273.002500')