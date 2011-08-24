# vim:fileencoding=utf-8

from common import \
    QueryPart, Targets, Where, And, Or, Join, JoinList, GroupBy, OrderBy, Limit

class Columns(QueryPart, list):
    def build(self):
        return ', '.join(self)

class From(QueryPart):
    def __init__(self, tables):
        self.tables = tables
    def build(self):
        return 'FROM ' + ', '.join(self.tables)
