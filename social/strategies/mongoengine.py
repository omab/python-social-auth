from mongoengine.queryset import OperationError

from social.strategies.dj import DjangoStrategy


class MongoengineStrategy(DjangoStrategy):
    def is_integrity_error(self, exception):
        return exception.__class__ is OperationError and \
               'E11000' in exception.message
