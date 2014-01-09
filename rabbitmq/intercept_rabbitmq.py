#!/usr/bin/env python

''' purpose : Intercepting messages that pass around nova-services directly from rabbitmq
    author: Prosunjit Biswas
    Date: Nov 8, 2013

'''

import pika
import sys
import json
from filter import conf_path, conf_value

from jsonpath_rw import jsonpath, parse
#import MessageFilter

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
        return self.parse_from_config(conf_path, conf_value)

def exchange_exists(exchange_name,exchg_type):
    print "exchange name is " + exchange_name
    if exchange_name.__len__() == 0:
      return False    
    parameters = pika.URLParameters('amqp://guest:admin@localhost:5672/%2F')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    try:   
      print channel.exchange_declare(exchange=exchange_name, exchange_type=exchg_type, passive=True).method
      if ( channel.exchange_declare(exchange=exchange_name, exchange_type=exchg_type, passive=True).method ):      
	  return True
      else:	  
	  return False
    except:	      
	  #print sys.exc_info()[0]
	  return False      

class OpenRabbit:
    messageno = 0
    def __init__(self):
        parameters = pika.URLParameters('amqp://guest:admin@localhost:5672/%2F')
        connection = pika.BlockingConnection(parameters)
        exchange_name="nova"
        queue_name = "simple_queue"
        binding_key = "#"

        channel = connection.channel()
        channel.exchange_declare(exchange = exchange_name,
                         type='topic')

        result = channel.queue_declare(exclusive=True)
        channel.queue_bind(exchange=exchange_name,
                   queue=queue_name,
                   routing_key=binding_key)

        print ' [*] Waiting for logs. To exit press CTRL+C'
        channel.basic_consume(self.callback,
                      queue=queue_name,
                      no_ack=True)

        channel.start_consuming()
        
        

    def nativecall(self, message):
        
        msg_params = MessageFilter(message=message).parse()
        print msg_params 
        #print msg_params['request_id'][0][4:]
        if exchange_exists(msg_params['msg_id'][0],"direct") == True :
	    print "----------exchange already exists-----------"+ msg_params['msg_id']
	    exit
	    
	if exchange_exists(msg_params['request_id'][0][4:],"direct") == True :	  
	    print "*********************exchange already exists-----------"+ msg_params['request_id']
	    exit 
	    

    def callback(self, ch, method, properties, body):

        self.messageno = self.messageno + 1
        print "\n\n"
        print ("----------------{}th message -----------------\n".format(self.messageno))
        print method.routing_key+"\n"
        print body
        
        #self.nativecall(body)
        #print body
        #print MessageFilter(body).parse()
        

def open_rabbit_test():
    OpenRabbit()
    
  

open_rabbit_test()

    