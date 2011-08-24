# vim:fileencoding=utf-8
import re

class QueryPart(object):
    def build(self):
        raise NotImplementedError('not implemented query part');

class Where(QueryPart, list):
    def build(self):
        return 'WHERE ' + ' '.join( c.build() for c in self )

class Condition(QueryPart):
    P_AND_OR = re.compile(r"\s(and|or)\s", re.I)
    def __init__(self, clause, *args):
        self.clause = clause
        self.args = args

    def build(self):
        if self.P_AND_OR.search( self.clause ) is not None:
            return '( ' + (self.clause % self.args) + ' )'
        else:
            return self.clause % self.args

class And(Condition):
    def build(self):
        return 'AND ' + Condition.build(self)

class Or(Condition):
    def build(self):
        return 'OR ' + Condition.build(self)

class Join(QueryPart):
    def __init__(self, table, jointype, clause, *args):
        self.table = table
        self.clause = clause
        self.args = args
        self.jointype = jointype

    def build(self):
        return '%s JOIN %s ON %s' % (
            self.jointype.upper(),
            self.table,
            (self.clause % self.args)
        )

class JoinList(list, QueryPart):
    def __init__(self):
        list.__init__(self)
    def build(self):
        return ' '.join(j.build() for j in self)


class GroupBy(QueryPart):
    def __init__(self, key):
        self.key = key
    def build(self):
        return 'GROUP BY %s' % self.key

class OrderBy(QueryPart):
    def __init__(self, key, ordertype='ASC'):
        self.key = key
        self.ordertype = ordertype
    def build(self):
        return 'ORDER BY %s %s' % (self.key, self.ordertype.upper())

class Limit(QueryPart):
    def __init__(self, limit, offset=None):
        self.limit = limit
        self.offset = offset
    def build(self):
        if self.offset is None:
            return 'LIMIT %d' % self.limit
        else:
            return 'LIMIT %d, %d' % (self.limit, self.offset)

class Target(QueryPart):
    def __init__(self, table):
        self.table = table
    def build(self):
        return self.table

class Targets(QueryPart, list):
    def __init__(self, arg):
        list.__init__(self, arg)
    def build(self):
        return ', '.join(self)
