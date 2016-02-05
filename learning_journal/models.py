from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime
    CheckConstraint
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True, mysql_length=255, CheckConstraint('title!=""'))
    body = Column(Text, default='')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, onupdate=datetime.datetime.utcnow)

    @classmethod
    def all(cls):
        all_entries = session.query(Entry).order_by(desc(Entry.id))
        return [(entry.title, entry.body) for entry in all_entries]

    @classmethod
    def by_id(cls, requested_id):
        return session.query(Entry).get(requested_id)
