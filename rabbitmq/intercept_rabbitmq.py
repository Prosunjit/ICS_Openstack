#!/usr/bin/env python

''' purpose : Intercepting messages that pass around nova-services directly from rabbitmq
    author: Prosunjit Biswas
    Date: Nov 8, 2013

'''

import pika
import sys
import json

from jsonpath_rw import jsonpath, parse
from MessageFilter import MessageFilter
from filter import rabbit_message_config

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

        print "declaring simple_queue "
	result = channel.queue_declare(queue=queue_name)
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
        #print body

        #self.nativecall(body)
        #print body
        print MessageFilter(message=body).parse(rabbit_message_config)
        

def open_rabbit_test():
    OpenRabbit()
    
  

open_rabbit_test()

    
