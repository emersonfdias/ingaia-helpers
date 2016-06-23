"""
    api.helpers.params
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements helpers for dealing with request parameters.
"""

import json

from flask import request, abort

from helpers.config import config
import helpers.common


def get_pagination():
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    
    if limit:
        limit = common.to_int(limit)
        if not (limit and 0 <= limit <= config.pagination.limit.max):
            limit = config.pagination.limit.default
    else:
        limit = config.pagination.limit.default

    if offset:
        offset = common.to_int(offset)
        if not (offset and 0 <= offset <= config.pagination.offset.max):
            offset = config.pagination.offset.default
    else:
        offset = config.pagination.offset.default
    
    return (limit, offset)


def get_expands(model):
    if request.args.get('expand') is None:
        return []
    else:
        return [expand for expand in request.args.get('expand').split(',')
                       if model.is_expandable(expand)]


def get_post_data(raise_error=True):
    try:
        data = json.loads(request.data)
        if not data:
            if raise_error:
                abort(400, 'The JSON cannot be empty')
            else:
                return None
        return data
    except ValueError:
        if raise_error:
            abort(400, 'Invalid JSON object')
        else:
            return None


def get_args_data(key, default_value=None):
    if key in request.args:
        return request.args[key]
    else:
        return default_value


def get_form_data(key, default_value=None):
    if key in request.form:
        return request.form[key]
    else:
        return default_value  