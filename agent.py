import time
import datetime

import sqlalchemy
import sqlalchemy.orm
import schema.listing


if __name__ == '__main__':
    engine = sqlalchemy.create_engine('')
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

        for listing in query:
            pass



        time.sleep(60)