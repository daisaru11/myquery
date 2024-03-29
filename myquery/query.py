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
    
        #if there is no condition, create a single condition and return
        if self._where is None:
            self._where = Where()
            self._where.append( Condition(clause, *args) )
            return self

        #create condition list
        self._where.append( And( Condition(clause, *args)) )
        return self

    def orwhere(self, clause, *args, **kargs):
        #escape literal args
        if kargs.get('escape') is not False:
            args = [self._dbconn.literal(arg) for arg in args]

        #if there is no condition, create a single condition and return
        if self._where is None:
            self._where = Where()
            self._where.append( Condition(clause, *args) )
            return self

        #create condition list
        self._where.append( Or( Condition(clause, *args)) )
        return self

    def where_in(self, col, vals, **kargs):
        #escape literal args
        if kargs.get('escape') is not False:
            vals = [self._dbconn.literal(val) for val in vals]

        #if there is no condition, create a single condition and return
        if self._where is None:
            self._where = Where()
            self._where.append( InCondition(col, vals) )
            return self

        #create condition list
        self._where.append( And(InCondition(col, vals)) )
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
