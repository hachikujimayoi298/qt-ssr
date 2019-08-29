import os
import sqlite3
from functools import partial

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import db_params

NonNull = partial(Column, nullable=False)
Base = declarative_base()


class ObservableQSqlDatabase(QObject, QSqlDatabase):

    def __init__(self, *args, **kwargs):
        self.onExecution = pyqtSignal()
        super(QSqlDatabase).__init__(*args, **kwargs)

    def exec(self, update=False, *args, **kwargs) -> QSqlQuery:
        res = super(QSqlDatabase).exec(*args, **kwargs)
        if update:
            self.onExecution.emit()
        return res

    def exec_(self, *args, **kwargs):
        return self.exec(*args, **kwargs)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = NonNull(Integer, primary_key=True)
    server = NonNull(String)
    group = NonNull(String, default=lambda ctx: 'Subscription %d' % ctx.get_current_parameters()['id'])


class Server(Base):
    __tablename__ = 'servers'
    id = NonNull(Integer, primary_key=True)
    server = NonNull(String)
    port = NonNull(Integer)
    password = NonNull(String)
    method = NonNull(String)
    protocol = NonNull(String)
    protocol_params = NonNull(String, default='')
    obfs = NonNull(String)
    obfs_params = NonNull(String, default='')
    remark = NonNull(String, default='')
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=True, default=None)
    subscription = relationship(Subscription, back_populates='servers')


Subscription.servers = relationship(Server, order_by=Server.id, back_populates='server')


def init_db(path):
    init = not os.path.isfile(path)
    if init:
        sqlite3.connect(path).close()

    database = QSqlDatabase("QSQLITE")
    database.setDatabaseName(path)

    database.open()

    def qt_exec(sql, *args, **kwargs):
        statement = sql.compile(dialect=mock.dialect)
        # print(statement)
        database.exec(str(statement))

    mock = create_engine('sqlite://', strategy='mock', executor=qt_exec)

    if init:
        Base.metadata.create_all(bind=mock)

    return database, mock


db, engine = init_db(db_params.path)
