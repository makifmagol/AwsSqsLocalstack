# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /AwsSqsLocalstack

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY database.ini .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
# create tables to store messages
CMD [ "python", "./create_table.py" ]