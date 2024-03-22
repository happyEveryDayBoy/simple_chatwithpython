import socket
import ds_protocol
import time


server = "168.235.86.101"
port = 3021

class DirectMessage:
  def __init__(self) -> None:
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username = None, password = None) -> None:
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password

  def send(self, message, recipient):
    '''
    The send function joins a ds server and sends a message

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    '''
  # try: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect(("168.235.86.101", port))
      join_msg = f'{{"join": {{"username": "{self.username}","password": "{self.password}" , "token":""}}}}'
      # '{"join": {"username": "ohhimark","password": "password123", "token":""}}'
      send = client.makefile('w')
      recv = client.makefile('r')
      send.write(join_msg + "\r\n")
      send.flush()
      jsontuple = recv.readline()
      tuple = ds_protocol.extract_json(jsontuple)
      response, text, *token = tuple
      token = token[0]

      if response == "ok" and message:

        entry_msg = f'{{"token": "{token}", "directmessage": {{"entry": "{message}", "recipient": "{recipient}", "timestamp":"{time.time()}"}}}}'
        # print(entry_msg)
        send.write(entry_msg + "\r\n")
        send.flush()
        # print(recv.readline())
        return True
      else:
        return False

  def retrieve_new(self):
    ''''
    Connects to the socket and uses the "new" command in the json
    string, iterates through the given list/dictionary to create a 
    list of the all new messages
    '''''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect(("168.235.86.101", port))
      join_msg = f'{{"join": {{"username": "{self.username}","password": "{self.password}" , "token":""}}}}'
      # '{"join": {"username": "ohhimark","password": "password123", "token":""}}'
      send = client.makefile('w')
      recv = client.makefile('r')
      send.write(join_msg + "\r\n")
      send.flush()
      jsontuple = recv.readline()
      tuple = ds_protocol.extract_json(jsontuple)
      response, text, *token = tuple
      token = token[0]
      new_req = f'{{"token": "{token}", "directmessage": "new"}}'
      send.write(new_req +"\r\n")
      send.flush()
      new_msgs = recv.readline()
      tuple = ds_protocol.extract_json(new_msgs)
      typ, messages, *token = tuple
      # print(messages)
      msgs = []
      for dics in messages:
        msg = dics['message']
        msgs.append(msg)
        # print(f'M {msgs}')
      # print(msgs)
      return msgs

  def retrieve_all(self):
    ''''
    Connects to the socket and uses the "all" command in the json
    string, interates through the dictionary/list to retreive all the 
    past messages
    '''
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect(("168.235.86.101", port))
      join_msg = f'{{"join": {{"username": "{self.username}","password": "{self.password}" , "token":""}}}}'
      # '{"join": {"username": "ohhimark","password": "password123", "token":""}}'
      send = client.makefile('w')
      recv = client.makefile('r')
      send.write(join_msg + "\r\n")
      send.flush()
      jsontuple = recv.readline()
      # print(jsontuple)
      tuple = ds_protocol.extract_json(jsontuple)
      response, text, *token = tuple
      token = token[0]
      all_req = f'{{"token": "{token}", "directmessage": "all"}}'
      send.write(all_req +"\r\n")
      send.flush()
      all_msgs = recv.readline()
      # print(all_msgs)
      # print(ds_protocol.extract_json(all_msgs))
      ttuple = ds_protocol.extract_json(all_msgs)
      # print(ttuple)
      typ, messages, *token = ttuple
      msgs = []
      for dic in messages:
        msg = dic['message']
        msgs.append(msg)
      # print(msgs)
      return msgs
