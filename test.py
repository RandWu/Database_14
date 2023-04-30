import api.sql as sql
import oracledb
import hashlib
connection = oracledb.connect(
    user="GROUP14",
    password="hd9qaY5L2t",
    dsn=oracledb.makedsn("140.117.69.60", 1521, service_name='ORCLPDB1')
)

db = sql.DB()
misc = sql.MISC()
student = sql.Students()
scholarship = sql.Scholarships()
cursor = db.connect()
a = misc.get_college()
b = scholarship.get_scholarship("1")
print(b)



# password = "P@s5w0rd"

# # Encode the password as bytes and hash it with SHA-1
# hash_object = hashlib.sha1(password.encode())

# # Get the hex digest (a string of hexadecimal digits) of the hash
# hash_hex = hash_object.hexdigest()

# print("SHA-1 hash of password:", hash_hex)
