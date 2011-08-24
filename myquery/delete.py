# vim:fileencoding=utf-8

from query import Query, QueryWhereMixIn
from querypart.delete import *

class DeleteQuery(Query, QueryWhereMixIn):
    def __init__(self, dbconn, table):
        Query.__init__(self, dbconn)

        self._where = None
        self._target = None

        self.target(table)


    def execute(self):
        sql = self._build_sql()
        return self._cursor.execute(sql)

    def get_sql(self):
        return self._build_sql()

    def _build_sql(self):
        if self._target is None:
            raise SQLBuildingError('no tables specified')

        str_buf = [ "DELETE", "FROM", self._target.build() ]
        if self._where is not None:
            str_buf.append( self._where.build() )

        return ' '.join(str_buf) + ';'

    def target(self, table):
        self._target = Target(table)
        return self


