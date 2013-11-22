from jsonpath_rw import jsonpath, parse
import json
from filter import conf

class MyJSON:
    pysondata = ""
    json_string = ""
    def __init__(self, file_name=None,string=None):
        self.json_string = self.readfile(file_name)
        if file_name:
            self.pysondata = self.readJSONfile(file_name)
        elif string:
             self.pysondata = self.readJSONfile(file_name)

    def readfile(self,file_name):
        with open (file_name, "r") as myfile:
            data=myfile.read()
            return data


    def readJSONfile(self,file_name):
        data = self.readfile(file_name)
        json_data = json.loads(data)
        self.pysondata = json_data
        return json_data

    def readFromJSONString(self,str):
        json_data = json.loads(str)
        self.pysondata = json_data
        return self.pysondata

    def parse_from_path(self,path):
        jsonpath_expr = parse(path)
        #print self.pysondata
        return [match.value for match in jsonpath_expr.find(self.pysondata)]

    def parse_from_config(self,config):
        # config is a dictionary
        config_values = {}
        for conf in config:
            config_values[conf] = self.parse_from_path(config[conf])

        return config_values
    def parse(self,config=None,path=None):
        if config :
            return self.parse_from_config(conf)
        elif path:
            return self.parse_from_path(path)


def testconf():
    my_json =  MyJSON(file_name="schedule_message.txt")
    print my_json.parse(config=conf)


#testconf()