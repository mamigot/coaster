'''
Utility functions for access to Postgres
'''


def get(session, model, model_field, value):
    item = session.query(model).filter(model_field == value).first()

    return item if type(item) is model else False
