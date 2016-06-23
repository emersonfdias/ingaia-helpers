"""
    api.helpers.cache
    ~~~~~~~~~~~~~~~~
    Implements Google App Engine Memcached Service.
"""

import os
import yaml
import pickle

from google.appengine.api import memcache

from api.helpers.config import config


def write(key, value, token=None):
    """Write a key/value pair to Google App Engine Memcached.
    If a token is specified, the key prefix will be token:<token>.
    """
    if value is not None:
        if token:
            memcache.set("token:%s:%s" % (token, key), value)
        else:
            memcache.set(key, value)


def read(key, token=None):
    """Read a value from Google App Engine Memcached.
    If a token is specified, the key prefix will be token:<token>.
    """
    if token:
        result = memcache.get("token:%s:%s" % (token, key))
    else:
        result = memcache.get(key)
    return result


def build_model_config_cache():
    for filename in os.listdir('api/models/config'):
        with open('api/models/config/%s' % filename, 'r') as yamlfile:
            model_config = yaml.load(yamlfile)
            prefix = 'model:%s' % filename.split('.')[0]
            write('%s:endpoint' % prefix, model_config.get('endpoint'))
            write('%s:url' % prefix, model_config.get('url'))
            mandatories = []
            for field, attributes in model_config['fields'].iteritems():
                for attribute, value in attributes.iteritems():
                    write('%s:%s:%s' % (prefix, attribute, field), value)
                    if attribute == 'mandatory':
                        mandatories.append(field)
            write('%s:mandatories' % prefix, pickle.dumps(mandatories))
            expands = model_config.get('expands')
            if expands:
                for expand in expands:
                    write('%s:expandable:%s' % (prefix, expand), True)
            filters = model_config.get('filters')
            if filters:
                write('%s:filters' % prefix, pickle.dumps(filters))
    write('model:built', True)
