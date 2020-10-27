from db_interface import DatabaseInterface
import os.path

import sqlite3

class SQLiteConn(DatabaseInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {}       # connections to databases
        self.cursors = {}           # open cursors
        self.selected_alias = None  # current selected connection

        self.conn = None            # current connection
        self.cursor = None          # current cursor

    def connect(self, path, alias):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.selected_alias = alias
        self.connections[alias] = self.conn
        self.cursors[alias] = self.cursor

    def get_selected_alias(self):
        return self.selected_alias

    def choose(self, alias):
        if alias not in self.connections or alias not in self.cursors:
            raise Exception('database alias ['+alias+'] not found')

        self.selected_alias = alias
        self.conn = self.connections[alias]
        self.cursor = self.cursors[alias]

    def exists(self, path):
        if os.path.exists(path):
            return True
        return False

    def shutdown(self, alias=None):
        alias = alias or self.selected_alias  # default to current connection

        try:
            self.cursors[alias].close()
            self.connections[alias].close()
            del self.cursors[alias]
            del self.connections[alias]
            #print('shutdown ['+alias+']')
        except KeyError:
            raise Exception('attempted to shutdown connection ['+alias+'] which was not defined')


    def shutdown_all(self):
        for alias in list(self.connections.keys()):
            self.shutdown(alias)


    def select(self, sql, fields=[]):
        self.cursor.execute(sql, fields)
        column = [a[0] for a in self.cursor.description]
        data = self.cursor.fetchall()

        result = []
        for obj in data:
            result.append(dict(zip(column, obj)))

        return result

    def execute(self, sql, fields=[]):
        self.cursor.execute(sql, fields)

    def insert_return_id(self, sql, fields=[]):
        self.cursor.execute(sql, fields)
        return self.cursor.lastrowid

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def _valid_ids(self, ids):
        for cur_id in ids:
            if not isinstance(cur_id, int):
                raise Exception('id passed [] was not an id')



    # ids can be single value or a list
    def load(self, table, ids=None):
        ids = ids or []
        # if single value not a list
        many = isinstance(ids, list)    # if getting a single record or many
        if not many:
            ids = [ids]     # convert to a list

        # Make sure that we are only excepting integers as ids
        self._valid_ids(ids)

        ids_str = ','.join([str(a) for a in ids])
        sql = "select * from %s where id in (%s)" % (table, ids_str)
        result = self.select(sql)

        # If many results expected
        if many:
            return result

        # One result expected
        if len(result) > 0:
            return result[0]

        # One result expected but not found
        return None


    def save(self, table, objs, id_column='id', force_id_insert=False):
        many = isinstance(objs, list)   # if list then saving many records

        if not many:
            objs = [objs]       # if many convert single object in a list

        result = []     # the result will a list of inserted ids

        # loop over my records to save
        for obj in objs:
            columns = []
            values = []
            obj_id = False

            # for each column in record
            for col in obj:
                val = obj[col]      # get the value of the column

                # search for id column
                if col == id_column:
                    obj_id = val            # get my id of the record if found
                    if not force_id_insert:
                        continue            # don't skip id column and value if force_insert on

                columns.append(col)     # collect all the columns to insert
                values.append(val)      # collect all the values to insert

            # if id null force_id_insert
            if not obj_id or force_id_insert:
                columns_str = ','.join([str(c) for c in columns])
                # create the number question marks needed to match the number of columns and values
                question_marks = []
                for val in range(0, len(values)):
                    question_marks.append('?')

                question_marks_str = ','.join(question_marks)   # create question mark string for insert statement

                sql = "insert into %s (%s) values(%s)" % (table, columns_str, question_marks_str)
                #print(sql)
                obj_id = self.insert_return_id(sql, values)
                #print(obj_id)

            else:
                update_clause = []      # used to store key value pair for update insert
                for col in columns:
                    update_clause.append(col+'=?')

                values.append(obj_id)
                update_clause_str = ','.join(update_clause)

                sql = "update %s set %s where id = %s" % (table, update_clause_str, '?')
                self.execute(sql, values)

            result.append(obj_id)      # build list of newly created row ids

        # if many records stored
        if many:
            return result

        # If single requested
        return result[0]



    # ids - single integer or list of integers
    def trash(self, table, ids=None):
        ids = ids or []
        many = isinstance(ids, list)

        if not many:
            ids = [ids]     # convert single id to a list

        self._valid_ids(ids)    # valid ids

        ids_str = ','.join([str(c) for c in ids])

        sql = 'delete from %s where id in (%s)' % (table, ids_str)
        self.execute(sql)

        if many:
            return ids

        return ids[0]      # technically still a string


    def dumpTable(self, table):
        sql = 'select * from '+table
        return self.select(sql)



if __name__ == '__main__':
    from pprint import pprint
    db_path = '../test_data/sqlite_test.db'
    db_path2 = '../test_data/sqlite_test2.db'

    db = SQLiteConn()
    # Test that exist method works
    if db.exists(db_path):
        print('database exists')
    else:
        print('creating new database at: '+db_path)


    # Connect to my databases
    db.connect(db_path, alias='test')       # connect my first test database
    #print('Selected DB: ', db.get_selected_alias())
    #db.connect(db_path2, alias='test2')     # connect second database
    #print('Selected DB: ', db.get_selected_alias())


    #db.choose('test')
    #print('Selected DB: ', db.get_selected_alias())


    rows = [
        {'name': 'One', 'lookup': 'own', 'status': 0},
        {'name': 'Two', 'lookup': 'two', 'status': 1},
        {'name': 'Three', 'lookup': 'three', 'status': 0},
        {'name': 'Four', 'lookup': 'four', 'status': 1},
    ]

    #db.save('test', rows)
    #db.commit()


    #sql = "insert into test (name, lookup, status) values(?, ?, ?)"
    #db.execute(sql, ['Four', 'four', True])
    #db.execute(sql, ['Five', 'five', False])
    #row_id = db.insert_return_id(sql, ['Six', 'six', True])
    #print('row_id: ', row_id)

    #obj = db.load('test', 2)
    #pprint(obj)
    #obj = db.load('test', [2,3,3,99,True])
    #pprint(obj)

    # Todo: finish testing save() method
    #objs = [
    #]
    #db.save('test', , id_column='id', force_id_insert=False):


    #db.commit()
    #db.rollback()

    #sql = "select * from test"
    #result = db.select(sql)
    #pprint(result)

    #db.trash('test', 1)
    #db.commit()

    #sql = 'select id from test'
    #result = db.select(sql)
    #ids = [a['id'] for a in result]

    #print(db.load('test', ids))

    # Delete all records
    if False:
        sql = 'select id from test'
        result = db.select(sql)
        ids = [a['id'] for a in result]
        print(ids)

        db.trash('test', ids)
        db.commit()

    #for row in db.dumpTable('test'):
    #    print(row)


    db.shutdown_all()

