'''
Utility functions for access to Postgres
'''
from models import institution, instructor, subject, \
    course, course_section, course_subsection, course_unit, course_video


def get_row(session, model, model_field, value):
    '''
    Gets object of row that matches the given value. If not present,
    returns False.
    '''
    item = session.query(model).filter(model_field == value).first()

    return item if type(item) is model else False


def get_or_create_row(session, model, model_field, value):
    '''
    Returns object if it exists using get_row(). Otherwise, instantiates
    a new one. It's up to the user to make sure that all required
    fields are added to the instantiated object before committing to the DB.
    '''
    existing = get_row(session, model, model_field, value)

    return existing if existing else model()


def get_row_from_parent(model, model_field_str, value, siblings):
    '''
    Returns object of row that matches the given value and is among the list of
    siblings (which are objects of similar type). If the object is not in the
    list, a fresh instance is initialized and returned.
    '''
    for s in siblings:
        if getattr(s, model_field_str) == value:
            return s

    return None


def get_or_create_row_from_parent(model, model_field_str, value, siblings):
    '''
    Returns object of row that matches the given value and is among the list of
    siblings (which are objects of similar type). If the object is not in the
    list, a fresh instance is initialized and returned.
    '''
    for s in siblings:
        if getattr(s, model_field_str) == value:
            return s

    return model()
