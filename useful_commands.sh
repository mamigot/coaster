# Generate SSH key
ssh-keygen -R 104.131.110.156

# Sync files across systems
rsync -aP --update --exclude '*.pyc' Coaster/ root@104.131.110.156:/home/mikel/coaster/

# View nginx's error log
cat /var/log/nginx/error.log

# List uwsgi processes
ps ax | grep uwsgi
# Once their PIDs are known, kill them by typing "kill PID"
