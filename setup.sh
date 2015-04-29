# -----------------------------------------------------------------------------#
# Add a user on Ubuntu with sudo privileges
# (consequently, the directory "/home/mikel/" will be created)
adduser mikel
# On visudo, add "mikel    ALL=(ALL:ALL) ALL" under "root    ALL=(ALL:ALL) ALL"
visudo
# -----------------------------------------------------------------------------#

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
sudo pip install virtualenvwrapper
# Add the virtualenvwrapper commands to the env. variables i.e.
# "source /usr/local/bin/virtualenvwrapper.sh" to "sudo nano ~/.bashrc"
source ~/.bashrc

# Make the virtualenv (specify the python version using "-p" if needed)
# mkvirtualenv --no-site-packages env-coaster

# Run the virtualenv
# workon env-coaster
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# pip install uwsgi flask

# Make sure that uWSGI can serve our application
# uwsgi -s coaster.sock --http 0.0.0.0:8000 --module app --callable app
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Log into Postgres user account (will not be able to access psql otherwise)
sudo -i -u postgres

# Within the console (psql), create a database:
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
# Use the DigitalOcean link for everything except the Redis version
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
# http://redis.io/download
sudo service redis_6379 start
sudo service redis_6379 stop
redis-cli

#(on Mac, start the Redis server by calling "redis-server"... Ctrl+C to exit)
# -----------------------------------------------------------------------------#


pip install -r requirements.txt

mkdir /home/mikel/coaster
cd /home/mikel/coaster/
