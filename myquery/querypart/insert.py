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


class Values(QueryPart, dict):
    def build(self, cols):
        try:
            return 'VALUES ( ' + ', '.join( self[c] for c in cols ) + ' )'
        except KeyError:
            raise SQLBuildingError('a column value is not specified')
            return None

class ValuesList(QueryPart, list):
    def build(self, cols):
        try:
            return 'VALUES ' + ', '.join( 
                '( ' + ', '.join( values[c] for c in cols ) + ' )' for values in self )
        except KeyError:
            raise SQLBuildingError('a column value is not specified')
            return None
