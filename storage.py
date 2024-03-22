import pathlib
import json
from ds_messenger import DirectMessage

class Storage:
    def __init__(self, username=None, password=None, data = [], server ="192.168.104.57"):
        self.username = username
        self.password = password
        self.dsuserver = server
        self.data = data
        self.port = 3021

    def format(self):
        ''''
        Converts the data parameter to the required format so it can be used in save_profile
        '''''
        lis = []
        if len(self.data) != 0:
            for data in self.data:
                convert = {data.recipient: [data.message, data.timestamp]}
                lis.append(convert)
            self.data = lis

    def save_profile(self, filepath, filename):
        ''''
        Works similarly to save_profile in the Profile module, creates a file and dumps the data into the file
        '''''
        self.format()
        path = pathlib.Path(filepath)
        if path.exists():
            if path.suffix == ".dsu" or path.is_dir():
                try:
                    if path.is_dir():
                        newpath = path/ f'{filename}.dsu'
                    newfile = open(newpath, 'w')
                    json.dump(self.__dict__, newfile)
                    newfile.close()
                except Exception as ex:
                    print(f"ERROR: {ex}")
        else:
            raise Exception


                
    def load_profile(self, filepath):
        ''''
        Loads the dumped data from the file and assigns the data to its proper variables
        '''''
        path = pathlib.Path(filepath)
        if path.exists() and path.suffix == ".dsu":
            newfile = open(path, 'r')
            data = json.load(newfile)
            self.username = data['username']
            self.password = data['password']
            self.dsuserver = data['dsuserver']
            for msg in data['data']:
                d = DirectMessage()
                for person, vals in msg.items():
                    d.recipient = person
                    d.message = vals[0]
                    d.timestamp = vals[1]
                    self.data.append(d)
        else:
            raise Exception
