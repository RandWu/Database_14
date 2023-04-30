import api.sql as sql
import oracledb

connection = oracledb.connect(
    user="GROUP14",
    password="hd9qaY5L2t",
    dsn=oracledb.makedsn("140.117.69.60", 1521, service_name='ORCLPDB1')
)

db = sql.DB()
misc = sql.MISC()
student = sql.Students()
cursor = db.connect()
a = misc.get_college()
data = student.get_role("1")
print(a)
print(type(data))