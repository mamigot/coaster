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
sudo pip install virtualenvwrapper
# Add the virtualenvwrapper commands to the env. variables i.e.
# "source /usr/local/bin/virtualenvwrapper.sh" to "sudo nano ~/.bashrc"
source ~/.bashrc

# Make the virtualenv
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
# createdb edx_courseware

# Access an existing database:
# psql edx_courseware

# \conninfo example (valid within psql):
# "You are connected to database "edx_courseware" as user "postgres" via
# socket in "/var/run/postgresql" at port "5432"."

# Reset user password on Postgres ("postgres" is the default user):
# http://stackoverflow.com/questions/14588212/resetting-password-of-postgresql-on-ubuntu

# Create tables by calling:
# python manage.py create_course_tables
# -----------------------------------------------------------------------------#


pip install -r requirements.txt

mkdir /home/mikel/coaster
cd /home/mikel/coaster/
