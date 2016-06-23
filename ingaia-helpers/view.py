"""
    api.helpers.view
    ~~~~~~~~~~~~~~~~~~~~~~~
    Implements helpers for views.
"""

from flask import request, jsonify

from api.helpers.config import config


def envelope(data, total=None, limit=config.pagination.limit.default,
             offset=config.pagination.offset.default):
    if type(data) == list:
        results = {
            'offset': offset,
            'total': total,
            'self': request.url,
            'data': data
        }
        if limit:
            results['limit'] = limit
    else:
        results = {
            'data': data
        }
    return jsonify(results)
