Prerequisite:
	 Install pika library for talking to rabbitmq
	 use : pip_install pika
	 Install jsonpath_rw
	 use: pip_install jsonpath_rw


File description:
   1. intercept_rabbitmq: This script intercept all rabbit messages that goes through "nova" exchange. Essentially it captures all rpc messages.
   2. receive_notification: This script intercept messages that goes to the notification.info queue. Essesntially, this is the messages of successful actions.


Run the script:
	python intercept_rabbitmq.py
