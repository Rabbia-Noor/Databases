"""STAGE 1: Deliberately hardcoded, disposable classroom credentials."""

import sys

import mysql.connector


def main() -> int:
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            database="school_mysql",
            user="mysql_student",
            password="MysqlDemoOnly123!",
            connection_timeout=5,
        )
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT environment FROM environment_info WHERE marker_key = %s", ("environment",))
            marker = cursor.fetchone()
            if marker is None or marker["environment"] != "dev":
                print("ERROR: MySQL database marker is incorrect; no student was written.", file=sys.stderr)
                return 1
            cursor.execute(
                "INSERT INTO students (roll_no, name) VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE name = %s",
                ("DEMO-001", "Ali", "Ali"),
            )
            connection.commit()
            cursor.execute("SELECT roll_no, name FROM students ORDER BY roll_no")
            print("Configuration source: hardcoded Python values")
            print("Connected to: dev | 127.0.0.1:3307")
            print("Database: school_mysql | marker: dev")
            for student in cursor.fetchall():
                print(f"Student: {student['roll_no']} | {student['name']}")
            print("PASS: student saved and read from MySQL.")
        return 0
    except mysql.connector.Error as error:
        if error.errno == 1045:
            print("ERROR: MySQL authentication failed.", file=sys.stderr)
        else:
            print("ERROR: MySQL connection or operation failed; check container health and setup.", file=sys.stderr)
        return 1
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
