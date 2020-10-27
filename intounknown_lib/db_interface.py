

class DatabaseInterface:
    def __init__(self):
        pass

    def connect(self, path, alias):
        pass

    def get_selected_alias(self):
        pass

    def choose(self, alias):
        pass

    def shutdown(self, alias):
        pass

    def shutdown_all(self):
        pass

    def select(self, sql, fields=[]):
        pass

    def execute(self, sql, fields=[]):
        pass

    def insert_return_id(self, sql, fields=[]):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def load(self, table, ids=None):
        ids = ids or []

    def save(self, table, objs, force_id_insert=False):
        objs = objs or []

    def trash(self, table, ids):
        ids = ids or []


