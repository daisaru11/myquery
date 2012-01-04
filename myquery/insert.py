# vim:fileencoding=utf-8

from query import Query, QueryWhereMixIn
from querypart.insert import *

class InsertQuery(Query):
    def __init__(self, dbconn, table):
        Query.__init__(self, dbconn)

        self._target = None
        self._cols = None
        self._values = None
        self._values_cache = None
        self._options = {}
        self._opt_allow = ['ignore']

        self.target(table)

    def execute(self):
        sql = self._build_sql()
        return self._cursor.execute(sql)

    def get_sql(self):
        return self._build_sql()

    def _build_sql(self):
        if self.target is None:
            raise SQLBuildingError('no tables specified')

        str_buf = [ 'INSERT', ]

        #option
        if 'ignore' in self._options and self._options['ignore']:
            str_buf.append( 'IGNORE' )

        str_buf.append( 'INTO' )
        str_buf.append( self._target.build() )

        #columns
        if self._cols is not None:
            str_buf.append( self._cols.build() )

        #values
        if self._values_cache is not None:
            if self._values is not None:
                self.next_row()
            str_buf.append( self._values_cache.build( self._cols ) )
        elif self._values is not None:
            str_buf.append( self._values.build( self._cols ) )

        return ' '.join(str_buf) + ';'

    def target(self, table):
        self._target = Target(table)
        return self

    def set(self, col, value, **kargs):
        if kargs.get('escape') is not False:
            value = self._dbconn.literal(value)

        if self._cols is None:
            self._cols = Columns()
        if col not in self._cols:
            self._cols.append(col)

        if self._values is None:
            self._values = Values()
        self._values[col] = value

        return self

    def set_opt(self, opt, value):
        opt = opt.lower()
        if opt in self._opt_allow:
            self._options[opt] = value

        return self

    def next_row(self):
        if self._values_cache is None:
            self._values_cache = ValuesList()
        self._values_cache.append( self._values )
        self._values = None

        return self

