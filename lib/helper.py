class _AttrDict(dict):
    """
    this class allows to use dictionaries in a object-like way.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
def _is_host(hosts,hostname):
    """
    returns true if a hostname is containied in a list
    of hosts.
    """
    for host in hosts:
        if hostname in host:
            return True
    return False

