import pika

credentials = pika.PlainCredentials("guest", "guest")

conn_params = pika.ConnectionParameters("localhost", 
    credentials = credentials)

# 1 - establish connection to broker
conn_broker = pika.BlockingConnection(conn_params)

# 2 - obtain channel
channel = conn_broker.channel()

# 3 - declare exhange
channel.exchange_declare(exchange="hello-exchange", 
    type="direct", passive=False, durable=True, auto_delete=False)

# 4 - declare queue
channel.queue_declare(queue="hello-queue")

# 5 - bind queue and exchange on key "hola"
channel.queue_bind(queue="hello-queue", 
    exchange="hello_exchange", routing_key="hola")

# 6 - function to process incoming messages
def msg_consumer(channel, method, header, body):

  # 7 - message acknowledgment
  channel.basic_ack(delivery_tag=method.delivery_tag)
   
  if body == "quit":
    # 8 - stop consuming and quit
    channel.basic_cancel(consumer_tag="hello-consumer")
    channel.stop_consuming()

  else:
    print body

  return

# 9 - subscribe consumer
channel.basic_consume(msg_consumer, queue="hello-queue", 
    consumer_tag="hello-consumer")

# 10 - start consuming
channel.start_consuming()
