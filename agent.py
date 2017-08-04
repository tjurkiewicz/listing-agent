import datetime
import os
import time

import pika
import sqlalchemy
import sqlalchemy.orm

import schema.listing
import proto.listing_pb2

def enqueue_listing_request(listing, ampq_channel, amqp_exchange):
    req = proto.listing_pb2.ListingRequest()
    req.id = listing.listing_id

    buffer = req.SerializeToString()

    ampq_channel.basic_publish(exchange=amqp_exchange,
                      routing_key='',
                      body=buffer)

if __name__ == '__main__':
    db_connection = os.environ.get('DB_CONNECTION')
    amqp_username = os.environ.get('AMQP_USERNAME')
    amqp_password = os.environ.get('AMQP_PASSWORD')
    amqp_host     = os.environ.get('AMQP_HOST')
    amqp_exchange = os.environ.get('AMQP_EXCHANGE')

    engine = sqlalchemy.create_engine(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    session = session_factory()

    while True:
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(hours=1)

        query = session.query(schema.listing.Listing) \
            .filter(sqlalchemy.or_(
                schema.listing.Listing.last_update == None,
                schema.listing.Listing.last_update < then
            )
        )

        credentials = pika.credentials.PlainCredentials(username=amqp_username, password=amqp_password)
        connection_params = pika.ConnectionParameters(host=amqp_host, credentials=credentials)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        for listing in query:
            enqueue_listing_request(listing, channel, amqp_exchange)

        connection.close()
        time.sleep(60)