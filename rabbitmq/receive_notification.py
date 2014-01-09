#!/usr/bin/env python
import pika
import sys
import json
from jsonpath_rw import jsonpath, parse

'''
input : matching_string: "includes(  scheduling, restart  )"
        beacon_word: "includes"
output: ['scheduling','restart']

this function match the beacon word, if the beacon_word is present, it removes the beacon_word and brackets and return
        remaining values splitted by commas

'''
def match_value_from_string(matching_string, beacon_word):
    matching_string = matching_string.lower()
    if beacon_word in  matching_string:
        string1 = matching_string.replace(beacon_word,"")
        string1 = string1.replace("(","")
        string1 = string1.replace(")","")
        t_values = string1.split(",")
        string_values = [str.strip() for str in t_values]
        return string_values
    return False

'''
Check if a String is a substring in a list of Strings
input: list: ["abc","def"]
       test_string: "abcd"
output: "abc".
'''

def is_superstring_of_a_string_from_list(list,test_string):
    for str in list:
        if str in test_string :
            return str
    return False



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
                print value
                print yes_list

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
    def parse(self):
        # using predefined configuration file here.
        from filter import  config
        #return self.parse_from_config(conf_path, conf_value)
        return self.parse_from_config(config)

class MessageBroker:

    def __init__(self):
        queue_name = 'notifications.info'
        parameters = pika.URLParameters('amqp://guest:admin@localhost:5672/%2F')
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue= queue_name)
        print ' [*] Waiting for messages. To exit press CTRL+C'
        channel.basic_consume(self.callback,
                              queue= queue_name,
                              no_ack=True)

        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        # the callback method body must not contain any file reference that is not included inside this script.
        # probably, this is a security requirement for PIKA library
        print MessageFilter(message=body).parse()
        print "\n"

def receive_message():
    MessageBroker()

receive_message()
#print "schuling" in return_value_from_string("includes(  scheduling, restart  )","includes")

