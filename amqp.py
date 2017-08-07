import contextlib

import pika

import config
import proto.listing_pb2


@contextlib.contextmanager
def publishing_channel():
    conf = config.get_config()

    amqp_host     = conf['Queue']['Host']
    amqp_username = conf['Queue']['Username']
    amqp_password = conf['Queue']['Password']

    credentials = pika.credentials.PlainCredentials(username=amqp_username, password=amqp_password)
    connection_params = pika.ConnectionParameters(host=amqp_host, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    yield channel

    channel.close()
    connection.close()


def enqueue_listing_request(listing_id, ampq_channel):
    conf = config.get_config()
    amqp_exchange = conf['Queue']['Exchange']

    req = proto.listing_pb2.ListingRequest()
    req.id = listing_id

    buffer = req.SerializeToString()

    ampq_channel.basic_publish(exchange=amqp_exchange,
                      routing_key='',
                      body=buffer)
