from django.utils.six import string_types


def to_js_value(key, value):
    if isinstance(value, string_types):
        return "'%s'" % value
    if isinstance(value, bool):
        return {True: 'true', False: 'false'}[value]
    return value
