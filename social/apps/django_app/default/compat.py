from django import VERSION

if VERSION >= (1, 8):
    from itertools import chain

    def get_all_field_names_from_options(opts):
        names = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
            for field in opts.get_fields()
            # For complete backwards compatibility, you may want to exclude
            # GenericForeignKey from the results.
            if not (field.many_to_one and field.related_model is None)
        )))
        return names
else:
    def get_all_field_names_from_options(opts):
        return opts.get_all_field_names()
