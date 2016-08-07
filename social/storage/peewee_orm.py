import six
import base64

from peewee import CharField, Model, Proxy, IntegrityError
from playhouse.kv import JSONField

from social.storage.base import UserMixin, AssociationMixin, NonceMixin, \
                                CodeMixin, BaseStorage


def get_query_by_dict_param(cls, params):
    query = True

    for field_name, value in params.iteritems():
        query_item = cls._meta.fields[field_name] == value
        query = query & query_item
        return query


database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class PeeweeUserMixin(UserMixin, BaseModel):
    provider = CharField()
    extra_data = JSONField(null=True)
    uid = CharField()
    user = None

    @classmethod
    def changed(cls, user):
        user.save()

    def set_extra_data(self, extra_data=None):
        if super(PeeweeUserMixin, self).set_extra_data(extra_data):
            self.save()

    @classmethod
    def username_max_length(cls):
        username_field = cls.username_field()
        field = getattr(cls.user_model(), username_field)
        return field.max_length

    @classmethod
    def username_field(cls):
        return getattr(cls.user_model(), 'USERNAME_FIELD', 'username')

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        if association_id is not None:
            query = cls.select().where(cls.id != association_id)
        else:
            query = cls.select().where(cls.provider != backend_name)
        query = query.where(cls.user == user)

        if hasattr(user, 'has_usable_password'):
            valid_password = user.has_usable_password()
        else:
            valid_password = True
        return valid_password or query.count() > 0

    @classmethod
    def disconnect(cls, entry):
        entry.delete_instance()

    @classmethod
    def user_exists(cls, *args, **kwargs):
        """
        Return True/False if a User instance exists with the given arguments.
        """
        user_model = cls.user_model()
        query = get_query_by_dict_param(user_model, kwargs)
        return user_model.select().where(query).count() > 0

    @classmethod
    def get_username(cls, user):
        return getattr(user, cls.username_field(), None)

    @classmethod
    def create_user(cls, *args, **kwargs):
        username_field = cls.username_field()
        if 'username' in kwargs and username_field not in kwargs:
            kwargs[username_field] = kwargs.pop('username')
        return cls.user_model().create(*args, **kwargs)

    @classmethod
    def get_user(cls, pk, **kwargs):
        if pk:
            kwargs = {'id': pk}
        try:
            return cls.user_model().select().get(
                get_query_by_dict_param(cls.user_model(), kwargs)
            )
        except cls.user_model().DoesNotExist:
            return None

    @classmethod
    def get_users_by_email(cls, email):
        user_model = cls.user_model()
        return user_model.select().where(user_model.email == email)

    @classmethod
    def get_social_auth(cls, provider, uid):
        if not isinstance(uid, six.string_types):
            uid = str(uid)
        try:
            return cls.select().where(
                cls.provider == provider, cls.uid == uid
            ).get()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_social_auth_for_user(cls, user, provider=None, id=None):
        query = cls.select().where(cls.user == user)
        if provider:
            query = query.where(cls.provider == provider)
        if id:
            query = query.where(cls.id == id)
        return list(query)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(uid, six.string_types):
            uid = str(uid)
        return cls.create(user=user, uid=uid, provider=provider)


class PeeweeNonceMixin(NonceMixin, BaseModel):
    server_url = CharField()
    timestamp = CharField()
    salt = CharField()

    @classmethod
    def use(cls, server_url, timestamp, salt):
        return cls.select().get_or_create(cls.server_url == server_url,
                                          cls.timestamp == timestamp,
                                          cls.salt == salt)


class PeeweeAssociationMixin(AssociationMixin, BaseModel):
    server_url = CharField()
    handle = CharField()
    secret = CharField()  # base64 encoded
    issued = CharField()
    lifetime = CharField()
    assoc_type = CharField()

    @classmethod
    def store(cls, server_url, association):
        try:
            assoc = cls.select().get(cls.server_url == server_url,
                                     cls.handle == association.handle)
        except cls.DoesNotExist:
            assoc = cls(server_url=server_url,
                        handle=association.handle)

        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    @classmethod
    def get(cls, *args, **kwargs):
        query = get_query_by_dict_param(cls, kwargs)
        return cls.select().where(query)

    @classmethod
    def remove(cls, ids_to_delete):
        cls.select().where(cls.id << ids_to_delete).delete()


class PeeweeCodeMixin(CodeMixin, BaseModel):
    email = CharField()
    code = CharField()  # base64 encoded
    issued = CharField()

    @classmethod
    def get_code(cls, code):
        try:
            return cls.select().get(cls.code == code)
        except cls.DoesNotExist:
            return None


class BasePeeweeStorage(BaseStorage):
    user = PeeweeUserMixin
    nonce = PeeweeNonceMixin
    association = PeeweeAssociationMixin
    code = PeeweeCodeMixin

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is IntegrityError
