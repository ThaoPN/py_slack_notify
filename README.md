# Methods
- post_message(channel_id, message, blocks, thread_ts, emoji)
- find_messages(channel_id, text)
- reaction(channel_id, emoji, ts)
- remove_reaction(channel_id, emoji, ts)
- edit_message(channel_id, message, blocks, ts, emoji)

## Example
### Post a message
```post_message(CHANNEL_ID, "Test a message", None, 'call_me_hand')```

### Make a reaction to a message
```reaction(CHANNEL_ID, 'tada', '1605086375.000900')```

### Find a message
```find_messages(CHANNEL_ID, "Test a message")```

### Edit a message
```edit_message(CHANNEL_ID, "Reply to message. This message has been edited", '1605089273.002500', 'call_me_hand')```

### Remove reaction on a message
```remove_reaction(CHANNEL_ID, 'call_me_hand', '1605089273.002500')```

## Install
```python setup.py bdist_wheel```

## Deploy
```python3 -m twine upload --repository pypi dist/*```

## Contribution
### Virtual environment
python3 -m venv venv
source venv/bin/activate