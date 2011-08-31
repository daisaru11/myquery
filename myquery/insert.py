# vim:fileencoding=utf-8

from query import Query, QueryWhereMixIn
from querypart.insert import *

class InsertQuery(Query):
    def __init__(self, dbconn, table):
        Query.__init__(self, dbconn)

        self._target = None
        self._cols = None
        self._values = None

        self.target(table)

    def execute(self):
        sql = self._build_sql()
        return self._cursor.execute(sql)

    def get_sql(self):
        return self._build_sql()

    def _build_sql(self):
        if self.target is None:
            raise SQLBuildingError('no tables specified')

        str_buf = [ 'INSERT', 'INTO', self._target.build() ]

        if self._cols is not None:
            str_buf.append( self._cols.build() )

        if self._values is not None:
            str_buf.append( self._values.build() )

        return ' '.join(str_buf) + ';'

    def target(self, table):
        self._target = Target(table)
        return self

    def set(self, col, value, **kargs):
        if kargs.get('escape') is not False:
            value = self._dbconn.literal(value)

        if self._cols is None:
            self._cols = Columns()
        self._cols.append(col)

        if self._values is None:
            self._values = Values()
        self._values.append(value)

        return self

