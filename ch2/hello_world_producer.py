import pika, sys

credentials = pika.PlainCredentials("guest", "guest")

conn_params = pika.ConnectionParameters("localhost", 
    credentials = credentials)

# 1 - establish connection to broker

conn_broker = pika.BlockingConnection(conn_params)

# 2 - obtain channel
channel = conn_broker.channel() 

# 3 - declare exchange
channel.exchange_declare(exchange="hello-exchange", type = "direct",
    passive=False, durable=True, auto_delete=False)

msg = sys.argv[1]
msg_props = pika.BasicProperties()

# 4 - create plaintext message
msg_props = content_type = "text/plain"

# 5 - publish message
channel.basic_publish(body=msg, exchange="hello-exchange", 
    properties=msg_props, routing_key="hola")
