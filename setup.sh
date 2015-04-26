# -----------------------------------------------------------------------------#
# Add a user on Ubuntu with sudo privileges
# (consequently, the directory "/home/mikel/" will be created)
adduser mikel
# On visudo, add "mikel    ALL=(ALL:ALL) ALL" under "root    ALL=(ALL:ALL) ALL"
visudo
# -----------------------------------------------------------------------------#


sudo apt-get update
sudo apt-get install python-pip python-dev nginx


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
pip install uwsgi flask

# Make sure that uWSGI can serve our application
# uwsgi -s coaster.sock --http 0.0.0.0:8000 --module app --callable app
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# Installing Postgres
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
sudo apt-get install postgresql postgresql-contrib

# Log into Postgres user account (will not be able to access psql otherwise)
sudo -i -u postgres

# Within the console (psql), create a database:
# createdb edx_courseware

# Access an existing database:
# psql edx_courseware
# -----------------------------------------------------------------------------#


mkdir /home/mikel/coaster
cd /home/mikel/coaster/
