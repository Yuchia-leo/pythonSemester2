import sqlite3

class DB:
    FORUM_DB = 'data/forum.db'
    FORUM_MAIN_TABLE = 'user'
    
    def __init__(self, db_name, main_table_name):
        self.db_name = db_name
        self.main_table_name = main_table_name
        self.init_db()

    def insert(self, sql, args):
        self.execute(sql, args)

    def insert_many(self, sql, args):
        conn = self.get_db_connection()
        conn.executemany(sql, args)
        conn.commit()
        conn.close()
    
    def select_one(self, sql, args):
        conn = self.get_db_connection()
        res = conn.execute(sql, args).fetchone()
        conn.commit()
        conn.close()
        return res
    
    def select_all(self, sql, args):
        conn = self.get_db_connection()
        res = conn.execute(sql, args).fetchall()
        conn.commit()
        conn.close()
        return res
    
    def update(self, sql, args):
        self.execute(sql, args)

    def delete(self, sql, args):
        self.execute(sql, args)
    
    def execute(self, sql, args):
        conn = self.get_db_connection()
        conn.execute(sql, args)
        conn.commit()
        conn.close()
        
    def execute_many(self, sql, args):
        conn = self.get_db_connection()
        res = conn.executemany(sql, args)
        conn.commit()
        conn.close()
        return res
    
    def execute_script(self, script):
        conn = self.get_db_connection()
        with open(script) as f:
            conn.executescript(f.read())
            conn.commit()
            conn.close()
    
    def init_db(self):
        sql = f"SELECT name FROM sqlite_master WHERE type = 'table' and name = '{self.main_table_name}'"
        args = ()
        table = self.select_one(sql, args)
        if not table:
            self.create_table()
            self.insert_data()

    def create_table(self): # each subclass must implement this method
        raise NotImplementedError("not implemented abstract method")
    
    def insert_data(self): # subclass can optionally implement this method to insert data
        pass

    def get_db_connection(self):
        conn = self.connect_to_db()
        conn.row_factory = sqlite3.Row
        return conn

    def connect_to_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error:
            print(f'failed on connect to DB: {self.db_name}')
