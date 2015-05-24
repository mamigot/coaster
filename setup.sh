#
# Software requirements (OS and Python-level packages + databases)
# in order to run the Coaster search engine
#


# -----------------------------------------------------------------------------#
# General packages: required for Python, PostgreSQL and nginx
# http://askubuntu.com/questions/499714/error-installing-scrapy-in-virtualenv-using-pip
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
# http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi
sudo apt-get update
sudo apt-get install python-pip python-dev nginx
sudo apt-get install libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Install Python-2.7.9 from source
sudo apt-get install build-essential libncursesw5-dev libreadline-gplv2-dev
sudo apt-get install libssl-dev libgdbm-dev libc6-dev libsqlite3-dev tk-dev
sudo apt-get build-dep python2.7

wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar -xvzf Python-2.7.9.tgz
cd Python-2.7.9/

./configure
make
make altinstall
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Set up virtualenvwrapper

sudo pip install virtualenvwrapper
# Add the virtualenvwrapper commands to the env. variables i.e.
# "source /usr/local/bin/virtualenvwrapper.sh" to "sudo nano ~/.bashrc"

# Make the virtualenv (specify the python version using "-p" if needed)
mkvirtualenv --no-site-packages env-coaster

# Run the virtualenv
workon env-coaster
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Required Python packages

# Install the following in order to get pyenchant to work
sudo apt-get install libenchant1c2a

pip install -r requirements.txt
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Initialize/Manage PostgreSQL database
# Log into Postgres user account (will not be able to access psql otherwise)
sudo -i -u postgres

# Within the console (type "psql" to access it), create a database:
> createdb edx_courseware

# Access an existing database:
psql edx_courseware

# "\conninfo" example (valid within psql):
# "You are connected to database "edx_courseware" as user "postgres" via
# socket in "/var/run/postgresql" at port "5432"."

# Reset user password on Postgres ("postgres" is the default user):
# http://stackoverflow.com/questions/14588212/resetting-password-of-postgresql-on-ubuntu

# Show database sizes: \l+
# Show table sizes: \d+

# Create tables by calling:
python manage.py create_course_tables
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Run the Selenium server via Docker to execute the crawling
docker pull selenium/standalone-chrome
export HOSTPORT=4444
export CONTAINERPORT=4444
docker run -p 127.0.0.1:$HOSTPORT:$CONTAINERPORT --name chromedriver -t -d selenium/standalone-chrome

# List all containers:
docker ps -a
# Stop, kill and remove a container:
docker stop chromedriver
docker kill chromedriver
docker rm chromedriver
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Initialize/Manage the Redis server

# Use the DigitalOcean link for everything except the Redis version
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
# http://redis.io/download
sudo service redis_6379 start
sudo service redis_6379 stop
redis-cli

#(on Mac, start the Redis server by calling "redis-server"... Ctrl+C to exit)

# In the Redis command line...
>> FLUSHDB # Delete all keys in the DB
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Install UWSGI and Flask (if not in requirements.txt)
pip install uwsgi flask

# If we get this message: "!!! no internal routing support, rebuild with pcre support !!!"
# go to http://stackoverflow.com/questions/21669354/rebuild-uwsgi-with-pcre-support

# Serve the application (later configure for nginx)
uwsgi -s app.sock --http 0.0.0.0:8000 --module app --callable app &
# Since it will be running in the background, use these commands to kill it
# ps -aux | grep uwsgi
# kill [pid of uwsgi process]
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Bonus/additional commands:

# Add a user on Ubuntu with sudo privileges ("/home/mikel/" will be created)
adduser mikel
# On visudo, add "mikel ALL=(ALL:ALL) ALL" under "root ALL=(ALL:ALL) ALL"
visudo

# monitor memory usage
sudo apt-get install htop
htop

# Generate SSH key
ssh-keygen -R 104.131.110.156

# Sync files across systems
rsync -aP --update --exclude '*.pyc' Coaster/ root@104.131.110.156:/home/mikel/coaster/

# View nginx's error log
cat /var/log/nginx/error.log

# Test nginx
sudo service nginx restart && curl http://104.131.110.156/ | \
grep "<head>" && sudo cat /var/log/nginx/error.log | tail -1
# -----------------------------------------------------------------------------#
