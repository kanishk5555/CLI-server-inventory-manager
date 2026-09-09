import sqlite3
import os
class Database:
    def __init__(self):
        db_path = os.getenv("DB_PATH", "inventory.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.createtable()
    
    def createtable(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers(
            hostname TEXT,
            ip TEXT,
            os TEXT,
            cpu INTEGER,
            ram INTEGER,
            disk INTEGER,
            location TEXT,
            status TEXT
        )
        """)
        self.conn.commit()
    def addserver(self,server):
        self.cursor.execute("""
        INSERT INTO servers
        (hostname, ip, os, cpu, ram, disk, location, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            server.host,
            server.ip,
            server.os,
            server.cpu,
            server.ram,
            server.disk,
            server.loc,
            server.stat
        ))
        self.conn.commit()
    def getallserver(self):
        self.cursor.execute("SELECT * FROM servers")
        return self.cursor.fetchall()
    def searchserver(self,host):
        self.cursor.execute("SELECT * FROM servers WHERE hostname=?",(host,))
        return self.cursor.fetchone()
    def updateserver(self,oldhost,newhost):
        self.cursor.execute("""
        UPDATE servers
        SET hostname=?
        WHERE hostname=?
        """,(newhost,oldhost))
        self.conn.commit()
    def switchstat(self,hname):
        self.cursor.execute("""
            UPDATE servers
            SET status = CASE
                WHEN status = 'Online' THEN 'Offline'
                ELSE 'Online'
            END
            WHERE hostname = ?
        """, (hname,))

        self.conn.commit()
    def deleteserver(self,host):
        self.cursor.execute("DELETE FROM servers WHERE hostname=?",(host,))
        self.conn.commit()
    def close(self):
        self.conn.close()
