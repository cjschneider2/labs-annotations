import os
try:
    import urlparse
    urlparse.uses_netloc.append("postgres")
    urlparse_f = urlparse.urlparse
except:
    import urllib.parse
    urllib.parse.uses_netloc.append("postgres")
    urlparse_f = urllib.parse.urlparse

import json
from peewee import (
    Model,
    SqliteDatabase,
    PostgresqlDatabase,
    TextField,
    CharField,
    DateTimeField,
)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    url = urlparse_f(DATABASE_URL)
    db = PostgresqlDatabase(
        url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
else:
    db = SqliteDatabase('db.db')


class Base(Model):
    class Meta:
        database = db


class Annotation(Base):
    url = CharField(index=True)
    data = TextField()
    created = DateTimeField(index=True)

    def __str__(self):
        return '<Annotation {url} {data}>'.format(
            url=self.url,
            data=self.data
        )

    def serialize(self):
        data = json.loads(self.data)
        data['id'] = self.id
        data['created'] = self.created.strftime('%b %d %H:%M'),
        return data


def init_tables():
    # db.drop_tables([Annotation], safe=True)
    db.create_tables([Annotation], safe=True)


if __name__ == '__main__':
    db.connect()
    init_tables()
    db.close()
