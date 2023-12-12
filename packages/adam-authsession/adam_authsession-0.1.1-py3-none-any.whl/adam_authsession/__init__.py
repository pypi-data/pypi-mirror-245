
__version__ = "0.0.1"
try:
    from adam_authsession import adam_authsession
except ImportError:
    pass

try:
    from adam_authsession.adam_authsession import adam_authsession  
except ImportError:
    pass    