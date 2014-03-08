#!/usr/bin/env python
import pika
import sys
import json
from jsonpath_rw import jsonpath, parse
from MessageFilter import MessageFilter

from filter import notification_message_config

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



'''
    This class connects to and fetches messages from the 'notifications.info' queue where each event of OpenStack  is reported.
'''
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
	load_message_config()
        print MessageFilter(message=body).parse(notification_message_config)
        print "\n"

def receive_message():
    MessageBroker()

receive_message()


