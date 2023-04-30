from typing import Optional
from datetime import datetime
from link import *

class DB():
    def connect(self):
        cursor = connection.cursor()
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
        connection.commit()

class Students():
    db = DB()
    def get_student(self, account):
        sql = "select trim(STUDID), STUNAME, STUSEX, ROLE from STUDENTS where trim(STUDID) = :id"
        return self.db.fetchall(self.db.execute_input(self.db.prepare(sql), {'id' : account}))
    
    def get_all_student(self):
        sql = "SELECT trim(STUDID) FROM STUDENTS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def create_student(self, userinput):
        sql = "INSERT INTO GROUP14.STUDENTS (STUDNAME, STUDSEX, STUself.dbIRTH, STUDGRADE, MAJID, DEPID, COID, ROLE) VALUES (:name, :sex, TO_DATE(':date', 'YYYY-MM-DD HH24:MI:SS'), '4', '2', '1', '1', :role)"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()
    
    def get_role(self, student_id):
        sql = "select ROLE, STUDNAME from STUDENTS where trim(STUDID) = :id"
        return self.db.fetchone(self.db.execute_input( self.db.prepare(sql), {'id':student_id}))
    
    def omit_student(self, student_id):
        sql = "delete from STUDENTS where trim(STUDID) = :id"
        self.db.execute_input(self.db.prepare(sql), student_id)
        self.db.commit()
    def apply_scholarship(self, userinput):
        current = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
        sql = f"insert into APPLY (SCHID, trim(STUDID), APPLYDATE) values (:schid, :studid, TO_DATE('{current}', 'YYYY-MM-DD HH24:MI:SS'))"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()

class Scholarships():
    db = DB()
    def get_scholarship(self, id):
        sql = 'SELECT * FROM SCHOLARSHIPS, APPLY where trim(STUDID) = :id and APPLY.SCHID = SCHOLARSHIPS.SCHID'
        return self.db.fetchall(self.db.execute_input(self.db.prepare(sql), {'id' : id}))
    
    def create_scholarship(self, userinput):
        sql = "INSERT INTO GROUP14.SCHOLARSHIPS (SCHNAME, SCHRANK, SCHYEAR, SCHISSUER) VALUES (:name, :rank, :year, :issuer)"
        self.db.execute_input(self.db.prepare(sql), userinput)
        self.db.commit()
    def omit_scholarships(self, id):
        sql = "delete from SCHOLARSHIPS where trim(SCHID) = :id"
        self.db.execute_input(self.db.prepare(sql), {"id": id})
        self.db.commit()

class MISC():
    db = DB()
    def get_college(self):
        sql = "select trim(COID), CONAME from COLLEGES"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def get_dept(self):
        sql = "select trim(DEPID), DEPNAME from DEPARTMENTS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    
    def get_major(self):
        sql = "select trim(MAJID), MAJNAME from MAJORS"
        return self.db.fetchall(self.db.execute(self.db.connect(), sql))
    

# class Analysis():
#     def month_price(i):
#         sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
#         return self.db.fetchall( self.db.execute_input( self.db.prepare(sql) , {"mon": i}))

#     def month_count(i):
#         sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
#         return self.db.fetchall( self.db.execute_input( self.db.prepare(sql), {"mon": i}))
    
#     def category_sale():
#         sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
#         return self.db.fetchall( self.db.execute( self.db.connect(), sql))

#     def member_sale():
#         sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
#         return self.db.fetchall( self.db.execute_input( self.db.prepare(sql), {'identity':'user'}))

#     def member_sale_count():
#         sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
#         return self.db.fetchall( self.db.execute_input( self.db.prepare(sql), {'identity':'user'}))