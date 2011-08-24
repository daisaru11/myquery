# vim:fileencoding=utf-8

import MySQLdb
from MySQLdb.cursors import DictCursor
from querypart.common import *

class SQLBuildingError(Exception):
    pass

class Query(object):
    def __init__(self, dbconn):
        self._dbconn = dbconn
        self._cursor = dbconn.cursor(DictCursor)

    def get_sql(self):
        return self._build_sql()

    def _build_sql(self):
        raise NotImplementedError('not implemented sql building');


class QueryWhereMixIn(object):
    def where(self, clause, *args, **kargs):
        #escape literal args
        if kargs.get('escape') is not False:
            args = [self._dbconn.literal(arg) for arg in args]
        self._where = Where()
        self._where.append( Condition(clause, *args) )
        return self
    
    def andwhere(self, clause, *args, **kargs):
        #if there is no condition, create a single condition and return
        if self._where is None:
            return self.where(clause, *args, **kargs)

        #escape literal args
        if kargs.get('escape') is not False:
            args = [self._dbconn.literal(arg) for arg in args]

        #create condition list
        self._where.append( And(clause, *args) )
        return self

    def orwhere(self, clause, *args, **kargs):
        #if there is no condition, create a single condition and return
        if self._where is None:
            return self.where(clause, *args, **kargs)

        #escape literal args
        if kargs.get('escape') is not False:
            args = [self._dbconn.literal(arg) for arg in args]

        #create condition list
        self._where.append( Or(clause, *args) )
        return self


class QueryJoinMixIn(object):
    def join(self, table, jointype, clause, *args, **kargs):
        #escape literal args
        if kargs.get('escape') is not False:
            args = [self._dbconn.literal(arg) for arg in args]

        if self._join is None:
            self._join = Join(table, jointype, clause, *args, **kargs)
            return self

        if isinstance(self._join, Join):
            _joinlist = JoinList()
            _joinlist.append(self._join)
            self._join = _joinlist

        self._join.append( Join(table, jointype, clause, *args) )
        return self
