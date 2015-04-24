FROM postgres

# http://www.slideshare.net/tarkasteve/developerweek-2015-docker-tutorial
ADD make-db.sh /docker-entrypoint-initdb.d/

RUN mkdir -p /code-utils-postgres
ADD . /code-utils-postgres/
WORKDIR /code-utils-postgres

CMD ["python", "manage.py", "create_course_tables"]
