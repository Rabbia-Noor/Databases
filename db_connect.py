import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="mysql_student",
    password="MysqlDemoOnly123!",
    database="school_mysql",
)

print("Connected to MySQL:", connection.database)
print("Server:", connection.server_host, connection.server_port)
cursor = connection.cursor()
cursor.execute("SELECT environment FROM environment_info")
print("Environment:", cursor.fetchone()[0])
cursor.close()
connection.close()
