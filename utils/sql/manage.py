import sys

'''
Creates course content tables on Postgres
'''
def create_course_tables():
    from main import Base, db_connect

    from main.models import institution, instructor, subject, \
        course, course_section, course_subsection, course_unit, course_video

    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    if sys.argv[1] == 'create_course_tables':
        create_course_tables()
