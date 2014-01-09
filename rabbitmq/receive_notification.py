#!/usr/bin/env python
import pika
import sys
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
    def parse_from_config(self,config, config_values):
        # config is a dictionary
        retrieve_values = {}
        for conf in config:
	    value = self.parse_from_path(config[conf])
	    if (config_values[conf].lower() == "any" ) or (value and value[0] == config_values[conf]):
	      retrieve_values[conf] = value


        return retrieve_values
    '''
        The json path to retrieve value from can be given as a config file, or as a dictionary containing paths
    '''
    def parse(self):
        # using predefined configuration file here.
        from filter import conf_path, conf_value
        return self.parse_from_config(conf_path, conf_value)

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

def receive_message():
    MessageBroker()

receive_message()

