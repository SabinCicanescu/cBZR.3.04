import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS invoice_record (
                invoice_number TEXT,
                invoice_value REAL,
                invoice_date TEXT,
                client_number TEXT,
                client_name TEXT,
                gl_account TEXT
            )
        """)
        self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def insertRecord(self, invoice_number, invoice_value, invoice_date, client_number, client_name, gl_account):
        self.cur.execute("INSERT INTO invoice_record VALUES (?, ?, ?, ?, ?, ?)",
                         (invoice_number, invoice_value, invoice_date, client_number, client_name, gl_account))
        self.conn.commit()

    def updateRecord(self, invoice_number, invoice_value, invoice_date, client_number, client_name, gl_account, rowid):
        self.cur.execute("""
            UPDATE invoice_record SET
                invoice_number = ?, invoice_value = ?, invoice_date = ?,
                client_number = ?, client_name = ?, gl_account = ?
            WHERE rowid = ?
        """, (invoice_number, invoice_value, invoice_date, client_number, client_name, gl_account, rowid))
        self.conn.commit()

    def removeRecord(self, rowid):
        self.cur.execute("DELETE FROM invoice_record WHERE rowid = ?", (rowid,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
