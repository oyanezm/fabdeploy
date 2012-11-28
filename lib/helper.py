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

def copy_keys(dict1,dict2):
    """
    copy keys from one dictionary to another
    """
    for key in dict2.keys(): dict1[key] = dict2[key]
