import json
import six

from django import VERSION
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

try:
    from django.utils.encoding import smart_unicode as smart_text
    smart_text  # placate pyflakes
except ImportError:
    from django.utils.encoding import smart_text

from social.utils import setting_name


if VERSION >= (1, 8):
    _JSONFieldBase = models.TextField
else:
    _JSONFieldBase = six.with_metaclass(models.SubfieldBase, models.TextField)

USE_POSTGRES_NATIVE_JSON_FIELD = getattr(settings, setting_name('USE_POSTGRES_NATIVE_JSON_FIELD'), False)

if USE_POSTGRES_NATIVE_JSON_FIELD:
    from django.contrib.postgres.fields import JSONField
else:
    class JSONField(_JSONFieldBase):
        """Simple JSON field that stores python structures as JSON strings
        on database.
        """

        def __init__(self, *args, **kwargs):
            kwargs.setdefault('default', '{}')
            super(JSONField, self).__init__(*args, **kwargs)

        # Support for Django < 1.8
        def to_python(self, value):
            """
            Convert the input JSON value into python structures, raises
            django.core.exceptions.ValidationError if the data can't be converted.
            """
            if self.blank and not value:
                return {}
            value = value or '{}'
            if isinstance(value, six.binary_type):
                value = six.text_type(value, 'utf-8')
            if isinstance(value, six.string_types):
                try:
                    # with django 1.6 i have '"{}"' as default value here
                    if value[0] == value[-1] == '"':
                        value = value[1:-1]

                    return json.loads(value)
                except Exception as err:
                    raise ValidationError(str(err))
            else:
                return value

        # Support for Django >= 1.8
        def from_db_value(self, value, expression, connection, context):
            """
            Convert the input JSON value into python structures, raises
            django.core.exceptions.ValidationError if the data can't be converted.
            """
            if self.blank and not value:
                return {}
            value = value or '{}'
            if isinstance(value, six.binary_type):
                value = six.text_type(value, 'utf-8')
            if isinstance(value, six.string_types):
                try:
                    # with django 1.6 i have '"{}"' as default value here
                    if value[0] == value[-1] == '"':
                        value = value[1:-1]

                    return json.loads(value)
                except Exception as err:
                    raise ValidationError(str(err))
            else:
                return value


        def validate(self, value, model_instance):
            """Check value is a valid JSON string, raise ValidationError on
            error."""
            if isinstance(value, six.string_types):
                super(JSONField, self).validate(value, model_instance)
                try:
                    json.loads(value)
                except Exception as err:
                    raise ValidationError(str(err))

        def get_prep_value(self, value):
            """Convert value to JSON string before save"""
            try:
                return json.dumps(value)
            except Exception as err:
                raise ValidationError(str(err))

        def value_to_string(self, obj):
            """Return value from object converted to string properly"""
            return smart_text(self.get_prep_value(self._get_val_from_obj(obj)))

        def value_from_object(self, obj):
            """Return value dumped to string."""
            return self.get_prep_value(self._get_val_from_obj(obj))


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [],
        ["^social\.apps\.django_app\.default\.fields\.JSONField"]
    )
except:
    pass
