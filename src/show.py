import psycopg2
from config import config

def retrieve_all_messages():
    sql = "select * from messages"
    conn = None
    
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the select statement
        cur.execute(sql)

        messages = cur.fetchall()

        for row in messages:
            print("MessageId = ", row[0], )
            print("Date = ", row[1])
            print("Message  = ", row[2], "\n")
            # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    retrieve_all_messages()
