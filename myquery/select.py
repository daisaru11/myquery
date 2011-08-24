# vim:fileencoding=utf-8

from query import Query, QueryWhereMixIn, QueryJoinMixIn
from querypart.select import *

class SelectQuery(Query, QueryWhereMixIn, QueryJoinMixIn):
    def __init__(self, dbconn, *tables):
        Query.__init__(self, dbconn)

        self._cols = None
        self._target = None
        self._where = None
        self._join = None
        self._groupby = None
        self._orderby = None
        self._limit = None

        self.target(*tables)

    def get_sql(self):
        return self._build_sql()

    def get_all(self):
        sql = self._build_sql()
        self._cursor.execute(sql)

        return self._cursor.fetchall()


    def get_one(self):
        sql = self._build_sql()
        self._cursor.execute(sql)

        return self._cursor.fetchone()

    def _build_sql(self):
        #check required sql parts
        if self._target is None:
            raise SQLBuildingError('no tables specified')
        if self._cols is None:
            self.select('*')

        #base
        str_buf = ['SELECT', self._cols.build(), 'FROM', self._target.build()]
        #join
        if self._join is not None:
            str_buf.append(self._join.build())
        #where
        if self._where is not None:
            str_buf.append(self._where.build())
        #group by
        if self._groupby is not None:
            str_buf.append(self._groupby.build())
        #order by
        if self._orderby is not None:
            str_buf.append(self._orderby.build())

        #limit
        if self._limit is not None:
            str_buf.append(self._limit.build())

        return ' '.join(str_buf) + ';'

    def select(self, *cols):
        self._cols = Columns(cols)
        return self

    def target(self, *tables):
        self._target = Targets(tables)
        return self

    def groupby(self, key):
        self._groupby = GroupBy(key)
        return self

    def orderby(self, key, ordertype='ASC'):
        self._orderby = OrderBy(key, ordertype)
        return self

    def limit(self, limit, offset=None):
        limit = int(limit)
        if offset is not None:
            offset = int(offset)
        self._limit = Limit(limit, offset)
        return self

