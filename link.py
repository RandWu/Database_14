import oracledb

connection = oracledb.connect(
    user="GROUP14",
    password="hd9qaY5L2t",
    dsn=oracledb.makedsn("140.117.69.60", 1521, service_name='ORCLPDB1')
)
