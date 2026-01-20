import pymysql
import os

def insert_records(records):
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database=os.environ['DB_NAME']
    )
    cursor = conn.cursor()

    for row in records:
        cursor.execute(
            "INSERT INTO user_data(name,email,age) VALUES (%s,%s,%s)",
            (row['name'], row['email'], row['age'])
        )

    conn.commit()
    conn.close()
