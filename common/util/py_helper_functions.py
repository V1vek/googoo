import logging    


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def remove_keys_with_value_none(query_filters):
    return dict((k, v) for k, v in query_filters.iteritems() if v)