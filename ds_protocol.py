
import json
from collections import namedtuple
import time


DataTuple = namedtuple('response', ['type','message', 'token'])



def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    if 'messages' in json_msg:
      # print(json_obj["response"])
      messages = json_obj['response']['messages']  
    else:
      messages = json_obj['response']['message']
    if type != 'error' and 'token' in json_msg:
        token = json_obj['response']['token']
    else:
        token = None
    return DataTuple(type, messages, token)
  
  except json.JSONDecodeError:
    print("Json cannot be decoded.")


# test = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'

# print(extract_json(test))
