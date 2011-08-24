# vim:fileencoding=utf-8

from common import \
    QueryPart, Target, Where, And, Or

class UpdateTarget(QueryPart):
    def __init__(self, table):
        self.table = table

    def build(self):
        return self.table

class Set(QueryPart):
    def __init__(self, col, value):
        self.col = col
        self.value = value

    def build(self):
        return self.col + ' = ' + self.value

class SetList(QueryPart, list):
    def build(self):
        return 'SET ' + ', '.join( s.build() for s in self )


