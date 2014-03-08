

'''
This class uses a configuration file to extract selected values from the json string.
It also implement selection based on positive and negative list of keywords.
'''

import json
from jsonpath_rw import jsonpath, parse

class MessageFilter:
    message_sanitization = True # we need to sanitize data before use
    from_file = None
    json_string = None
    def __init__(self, file_name=None,message=None):
        if file_name:
            from_file = True
            self.pysondata = self.readJSONfile(file_name)
        elif message:
            if self.message_sanitization == True:
                message = self.sanitize(message)
            self.pysondata = self.readFromJSONString(message)

    def sanitize(self, message):
        # replace "//" with "" which has been added by oslo messaging
        message = message.replace("\\","")
        # oslo adds extra  sign (") in two different places. Removing them out here.
        message = message.replace('"oslo.message": "{','')
        message = message.replace('}", "oslo.version": "2.0"','')
        return message
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
        retrieve_values = {}
        for j_path in config:
            value = self.parse_from_path(j_path)
            if value.__len__() == 0:
                continue
            elif (config[j_path].lower() == "any" ):
                retrieve_values[j_path] = value[0]
            elif "includes" in  config[j_path].lower():
                yes_list = match_value_from_string(config[j_path].lower(),"includes")
                if is_superstring_of_a_string_from_list(yes_list,value[0]) is not False:
                    retrieve_values[j_path] = value[0]
            elif "does_not_include" in  config[j_path].lower():
                no_list = match_value_from_string(config[j_path].lower(),"does_not_include")
                if is_superstring_of_a_string_from_list(no_list,value[0]) is False:
                    retrieve_values[j_path] = value[0]

        return retrieve_values


    '''
        The json path to retrieve value from can be given as a config file, or as a dictionary containing paths
    '''
    def parse(self,config):
        # using predefined configuration file here.
        #from filter import  config
        #return self.parse_from_config(conf_path, conf_value)
	#return self.pysondata
        return self.parse_from_config(config)
