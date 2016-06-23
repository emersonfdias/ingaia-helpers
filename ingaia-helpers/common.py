"""
    api.helpers.common
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements common Python helpers.
"""


def to_int(arg):
    try:
        return int(arg)
    except ValueError:
        return None


def get_key(dict, key):    
    try:
        return dict[key]
    except KeyError:
        return None


def not_empty(str_value):
    try:
        return (str_value and str_value.strip())
    except:
        return None
