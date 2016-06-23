"""
    api.helpers.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements project configuration helpers.
"""

import yaml

class Dotable(dict):
    __getattr__= dict.__getitem__

    def __init__(self, d):
        self.update(**dict((k, self.parse(v))
                           for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v


def env():
    from google.appengine.api.app_identity import get_application_id
    appname = get_application_id()
    if appname.find('-development') > 0 or appname.find('-dev') > 0:
        return 'dev'
    elif appname.find('-staging') > 0 or appname.find('-st') > 0:
        return 'staging'
    else:
        return 'prod'


def version():
    import os; return os.environ['CURRENT_VERSION_ID']


with open('config/%s.yaml' % env(), 'r') as yamlfile:
    config = Dotable.parse(yaml.load(yamlfile))   
