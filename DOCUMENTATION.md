-all codes located in src folder
-database.ini contains postgres connection config
-requirenments.txt contains python packages need to be install to run the app
-database creation is located in docker-compose.yml
-dockerfile contains environment setup and create table script

Tool has been written with Python. There are 3 python files for this task. comsume.py takes an integer argument (10 by default) and retrieves the given number of messages and stores them to postgres db. show.py lists all messages stores in db. clear.py delete all messages in db.

To run the tool:
1- docker-compose up
2- docker build -t message_tool .
3- python consume [--count n] | show | clear