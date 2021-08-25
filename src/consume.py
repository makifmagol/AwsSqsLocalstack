from os import access
import boto3
import argparse
import psycopg2
from config import config
from datetime import date

# Create SQS client
sqs = boto3.client(
    'sqs', 
    region_name="ap-southeast-1",
    aws_access_key_id="test-key",
    aws_secret_access_key="test-secret")

queue_url = 'http://localhost:4566'

def consume_store_messages():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    message_id = message['MessageId']
    message_content = message['Body']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
    insert_message(message_id, date.today(),message_content)

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument("-c", "--count", help="Number of element", type=int, default=10)
    
    # Parse arguments
    args = parser.parse_args()

    return args

def insert_message(message_id,message_date,message):
    """ insert a new message into the messages table """
    sql = """INSERT INTO messages(message_id,date,content)
             VALUES(%s,%s,%s) RETURNING message_id;"""
    conn = None
    message_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (message_id,message_date,message))
        # get the generated id back
        message_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return message_id

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()

    for i in range(args.__dict__["count"]):
        consume_store_messages()