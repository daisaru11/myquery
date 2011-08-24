# vim:fileencoding=utf-8

from query import Query, QueryWhereMixIn
from querypart.update import *

class UpdateQuery(Query, QueryWhereMixIn):
    def __init__(self, dbconn, table):
        Query.__init__(self, dbconn)

        self._target = None
        self._set = None
        self._where = None

        self.target(table)

    def get_sql(self):
        return self._build_sql()

    def execute(self):
        sql = self._build_sql()
        result = self._cursor.execute(sql)
        self._dbconn.commit()
        return result

    def _build_sql(self):
        if self._target is None:
            raise SQLBuildingError('no tables specified')

        if self._set is None:
            raise SQLBuildingError('no columns specified')


        str_buf = [ 'UPDATE', self._target.build(), self._set.build() ]

        if self._where is not None:
            str_buf.append( self._where.build() )

        return ' '.join(str_buf) + ';'

    def target(self, table):
        self._target = Target(table)

    def set(self, col, value, **kargs):
        if kargs.get('escape') is not False:
            value = self._dbconn.literal(value)

        if self._set is None:
            self._set = SetList()

        self._set.append( Set(col, value) )

        return self

