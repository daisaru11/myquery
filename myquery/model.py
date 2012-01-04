# vim:fileencoding=utf-8

import MySQLdb
from MySQLdb.cursors import DictCursor
from select import SelectQuery
from insert import InsertQuery
from update import UpdateQuery
from delete import DeleteQuery

class Model(object):
    dbconn = None
    _instances = dict()
    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls is Model:
            raise NotImplementedError, 'Base Model class instance should not be generated.'
        return Model._instances.get(hash(cls)) or\
            Model._instances.setdefault(hash(cls), cls())

    @staticmethod
    def setDbConn(dbconn):
        Model.dbconn = dbconn

    def selectQuery(self, table):
        return SelectQuery(self.dbconn, table)

    def insertQuery(self, table):
        return InsertQuery(self.dbconn, table)

    def deleteQuery(self, table):
        return DeleteQuery(self.dbconn, table)

    def updateQuery(self, table):
        return UpdateQuery(self.dbconn, table)

    @staticmethod
    def execute(sql):
        cursor = Model.dbconn.cursor(DictCursor)
        cursor.execute(sql)
        return cursor

    @staticmethod
    def commit():
        return Model.dbconn.commit()

    @staticmethod
    def rollback():
        return Model.dbconn.rollback()

