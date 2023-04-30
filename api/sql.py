from typing import Optional
from datetime import datetime
import link
import utilities as u

class DB():
    def connect(self):
        cursor = link.connection.cursor()
        return cursor

    def prepare(self, sql):
        cursor = self.connect()
        cursor.prepare(sql)
        return cursor

    def execute(self, cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(self, cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(self, cursor):
        return cursor.fetchall()

    def fetchone(self, cursor):
        return cursor.fetchone()

    def commit(self):
        link.connection.commit()

class Students():
    db = DB()
    def get_student(self, account: str) -> Optional[list]:
        sql = "select trim(STUDID), STUNAME, STUSEX, ROLE from STUDENTS where trim(STUDID) = :id"
        return self.db.fetchall(self.db.execute_input(self.db.prepare(sql), {'id' : account}))
    
    def get_all_student(self) -> Optional[list]:
        sql = "SELECT trim(STUDID), STUDNAME, ROLE FROM STUDENTS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def create_student(self, userinput: dict):
        sql = "INSERT INTO GROUP14.STUDENTS (STUDNAME, STUDSEX, STUDBIRTH, STUDGRADE, MAJID, DEPID, COID, ROLE, PASSWD) VALUES (:name, :sex, TO_DATE(':date', 'YYYY-MM-DD HH24:MI:SS'), '4', '2', '1', '1', :role, :password)"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()
    
    def get_role(self, student_id: str) -> Optional[tuple]:
        sql = "select ROLE, STUDNAME from STUDENTS where trim(STUDID) = :id"
        return self.db.fetchone(self.db.execute_input( self.db.prepare(sql), {'id':student_id}))
    
    def omit_student(self, student_id: str):
        sql = "delete from STUDENTS where trim(STUDID) = :id"
        self.db.execute_input(self.db.prepare(sql), student_id)
        self.db.commit()

    def apply_scholarship(self, userinput: dict):
        current = u.datetime_format(u.get_current_time())
        sql = f"insert into APPLY (SCHID, trim(STUDID), APPLYDATE) values (:schid, :studid, TO_DATE('{current}', 'YYYY-MM-DD HH24:MI:SS'))"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()

    def fetch_login_info(self, name: str) -> Optional[tuple]:
        sql = "select STUDNAME, PASSWD, ROLE, trim(STUDID) from STUDENTS where STUDNAME = :name"
        return self.db.fetchone(self.db.execute_input(self.db.prepare(sql), {'name':name}))

class Scholarships():
    db = DB()
    def get_scholarship(self, id: str) -> Optional[list]:
        sql = 'SELECT * FROM SCHOLARSHIPS where trim(SCHID) = :id'
        return self.db.fetchall(self.db.execute_input(self.db.prepare(sql), {'id' : id}))
    
    def get_all_scholarship(self) -> Optional[list]:
        sql = "SELECT trim(SCHID), SCHNAME, SCHRANK, SCHYEAR, SCHISSUER from SCHOLARSHIPS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def create_scholarship(self, userinput: dict):
        sql = "INSERT INTO GROUP14.SCHOLARSHIPS (SCHNAME, SCHRANK, SCHYEAR, SCHISSUER) VALUES (:name, :rank, :year, :issuer)"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()
    
    def update_scholarship(self, userinput: dict):
        sql = "UPDATE SCHOLARSHIPS SET SCHNAME = :name, SET SCHRANK = :rank, SET SCHYEAR = :year, SET SCHISSUER = :issuer WHERE TRIM(SCHID)=:id;"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()

    def omit_scholarships(self, id: str):
        sql = "delete from SCHOLARSHIPS where trim(SCHID) = :id"
        self.db.execute_input(self.db.prepare(sql), {"id": id})
        self.db.commit()
    
    def is_omit_okay(self, id: str) -> bool:
        sql = "select * from APPLY where trim(SCHID) = :id"
        result =  self.db.fetchone(self.db.execute_input(self.db.prepare(sql), {'id' : id}))
        return result is None

class MISC():
    db = DB()
    def get_college(self) -> Optional[list]:
        sql = "select trim(COID), CONAME from COLLEGES"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def get_dept(self) -> Optional[list]:
        sql = "select trim(DEPID), DEPNAME from DEPARTMENTS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def get_major(self) -> Optional[list]:
        sql = "select trim(MAJID), MAJNAME from MAJORS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))

class Analysis():
    db = DB()

    def placeholder(self):
        # placeholder
        pass