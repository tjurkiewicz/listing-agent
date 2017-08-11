import datetime
import logging
import time

import sqlalchemy.orm

import amqp
import config
import schema.listing


if __name__ == '__main__':
    config.setup()
    conf = config.get_config()

    logging.info("listing agent is starting.")

    db_connection = conf['SQLDatabase']['Connection']
    interval = conf.getint('Runtime', 'Interval')

    engine = sqlalchemy.create_engine(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    session = session_factory()

    while True:
        with amqp.publishing_channel() as ch:
            now = datetime.datetime.utcnow()
            then = now - datetime.timedelta(hours=1)

            query = session.query(schema.listing.Listing) \
                .filter(sqlalchemy.or_(
                    schema.listing.Listing.last_update == None,
                    schema.listing.Listing.last_update < then
                )
            )

            for listing in query:
                amqp.enqueue_listing_request(listing.listing_id, ch)

            time.sleep(interval)
