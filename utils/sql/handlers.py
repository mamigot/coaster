'''
Utility functions for access to Postgres
'''

def get_column_value(session, row_object, property_name):
    '''
    Gets value of property from model instance corresponding to a
    given row.
    '''
    pass


def get_row(session, model, model_field, value):
    '''
    Gets object of row that matches the given value. If not present,
    returns False.
    '''
    item = session.query(model).filter(model_field == value).first()

    return item if type(item) is model else False
