"""
This module contains classe for all DB operaions in the app.
They are as below:
    BaseAbstraction
    UserAbstraction
    BookAbstraction
    AuthorAbstraction

The BaseAbstraction class contains all the low-level operations with ORM.
Other classes provide interfaces for corresponding model
"""

from sqlalchemy import exc


def safe_execute(method):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, DBObject):
            raise TypeError(
                '@safe_execute should be applied inside BaseAbstraction '
                'subclasses only'
            )
        on_success = kwargs.pop('on_success', self.save)
        on_failure = kwargs.pop('on_failure', self.revert)

        try:
            if method:
                res = method(self, *args, **kwargs)
                on_success()
                return res
            on_success()
        except exc.IntegrityError, err:
            on_failure()
            raise err

    return wrapper


class DBObject(object):
    """
    Base class for other abstractions. All low-level operations like
    creating, updating or deleting objects to/from DB should be defined here
    """

    model = None
    session = None

    @safe_execute
    def create(self, **kwargs):
        new_entry = self.model()

        for key in kwargs.iterkeys():
            setattr(new_entry, key, kwargs[key])

        self.session.add(new_entry)
        return new_entry

    @safe_execute
    def delete(self, **kwargs):
        entry_obj = self.model().query.get(kwargs.get('id'))
        if entry_obj:
            self.session.delete(entry_obj)

    @safe_execute
    def update(self, entry_obj, **kwargs):
        for key in kwargs.iterkeys():
            if hasattr(entry_obj, key):
                setattr(entry_obj, key, kwargs[key])

        self.session.add(entry_obj)

    def get(self, id):
        return self.model.query.get(id)

    def get_one(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).one()

    def get_all(self, **kwargs):
        if kwargs:
            return self.session.query(self.model).filter_by(**kwargs).all()
        else:
            return self.session.query(self.model).all()

    def save(self):
        self.session.commit()

    def revert(self):
        self.session.rollback()


