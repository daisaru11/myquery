# vim:fileencoding=utf-8

from common import \
    QueryPart, Target

class Into(QueryPart):
    def __init__(self, table):
        self.table = table
    def build(self):
        return 'INTO ' + self.table


class Columns(QueryPart, list):
    def build(self):
        return '( ' + ', '.join(self) + ' )'


class Values(QueryPart, list):
    def build(self):
        return 'VALUES ( ' + ', '.join(self) + ' )'
