# vim:fileencoding=utf-8
from MySQLdb import MySQLError
from select import SelectQuery
from insert import InsertQuery
from update import UpdateQuery
from delete import DeleteQuery
import datetime

class ModelProcessingError(Exception):
    pass

class Model(object):
    _instances = {}
    _dbconn = None
    _current = None
    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        return cls._instances.get(cls.__name__) or\
            cls._instances.setdefault(cls.__name__, cls())

    @staticmethod
    def setDbConn(dbconn):
        Model._dbconn = dbconn

    @property
    def current(self):
        if self._current is None:
            self._current = datetime.datetime.now()
        return self._current

    def selectQuery(self, table):
        return SelectQuery(self._dbconn, table)

    def insertQuery(self, table):
        return InsertQuery(self._dbconn, table)

    def deleteQuery(self, table):
        return DeleteQuery(self._dbconn, table)

    def updateQuery(self, table):
        return UpdateQuery(self._dbconn, table)

    def insert_id(self):
        return self._dbconn.insert_id()


#decorator
def check_mysql_exception(func):
    def _(*args, **kargs):
        try:
            return func(*args, **kargs)
        except MySQLError, e:
            m = 'Raise MySQL exception:%s' % repr(e)
            raise ModelProcessingError(m)
    return _

