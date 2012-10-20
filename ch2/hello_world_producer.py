import pika, sys
from pika import spec

credentials = pika.PlainCredentials("guest", "guest")

conn_params = pika.ConnectionParameters("localhost", 
    credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel()

# 1 - publish confirm handler
def confirm_handler(frame):

  if type(frame.method) == spec.Confirm.SelectOk:
    print "Channel in 'confirm' mode."

  elif type(frame.method) == spec.Basic.Nack:
    if frame.method.delivery_tag in msg_ids:
      print "message lost!"

  elif type(frame.method) == spec.Basic.Ack:
    if frame.method.delivery_tag in msg_ids:
      print "confirm received"
      msg_ids.remove(frame.method.delivery_tag)

# 2 - put channel in confirm mode
channel.confirm_delivery(callback=confirm_handler)

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# 3 - reset message ID tracker
msg_ids = []

# 4 - publish message
channel.basic_publish(body=msg, 
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola")

# 5 - add ID to tracking list
msg_ids.append(len(msg_ids) + 1)
channel.close()
