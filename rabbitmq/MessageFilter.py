from jsonpath_rw import jsonpath, parse
import json
'''
    filter.py contains the json paths  that we want to know value of
'''
from filter import conf

class MessageFilter:
    from_file = None
    json_string = None
    def __init__(self, file_name=None,message=None):
        if file_name:
            from_file = True
            self.pysondata = self.readJSONfile(file_name)
        elif message:
             self.pysondata = self.readFromJSONString(message)

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

    def parse_from_file(self):
        pass
    def parse_from_config(self,config):
        # config is a dictionary
        config_values = {}
        for conf in config:
            config_values[conf] = self.parse_from_path(config[conf])

        return config_values
    '''
        The json path to retrieve value from can be given as a config file, or as a dictionary containing paths
    '''
    def parse(self):
        return self.parse_from_config(conf)


def testconf():
    my_filter =  MessageFilter(file_name="schedule_message.txt")
    print my_filter.parse()


#testconf()