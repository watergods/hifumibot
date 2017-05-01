"""
Useful helper functions
"""
from os.path import join


def combine_dicts(dicts):
    """
    combine (nested) dictionaries with numbers as values,
    assuming same key in all dicts maps to the same data type
    :param dicts: an iterable of dicts
    :return: the combined dict
    >>> d1 = {'a': 1, 'b': 2}
    >>> d2 = {'a': 1, 'c':1}
    >>> d3 = combine_dicts((d1, d2))
    >>> d3 == {'a': 2, 'b': 2, 'c': 1}
    True
    >>> d4 = {'d1': d1, 'd2': d2}
    >>> d5 = {'d1': d1, 'c':100}
    >>> d6 = combine_dicts((d4, d5))
    >>> d6 == {'d1': {'a': 2, 'b': 4}, 'd2': d2, 'c': 100}
    True
    >>> combine_dicts((d1, d2, d3)) == {'a': 4, 'b': 4, 'c': 2}
    True
    >>> combine_dicts((d4, d5, d6)) == \
    {'d1':{'a': 4,'b':8}, 'd2': {'a':2,'c':2}, 'c': 200}
    True
    """
    if len(dicts) == 0:
        return None
    elif len(dicts) == 1:
        return dicts[0]
    elif len(dicts) == 2:
        d1, d2 = dicts
        res = {}
        all_keys = set(list(d1.keys()) + list(d2.keys()))
        for key in all_keys:
            if key in d1 and key in d2:
                if isinstance(d1[key], dict):
                    res[key] = combine_dicts((d1[key], d2[key]))
                else:
                    a, b = d1[key], d2[key]
                    if a is not None and b is not None:
                        s = a + b
                    elif a is not None:
                        s = a
                    else:
                        s = b
                    res[key] = s
            elif key in d1:
                res[key] = d1[key]
            elif key in d2:
                res[key] = d2[key]
        return res
    elif len(dicts) > 2:
        l = len(dicts)
        return combine_dicts(
            (combine_dicts(dicts[:l // 2]), combine_dicts(dicts[l // 2:])))


def get_distro():
    """
    You linux distro version info.
    """
    raw = ' '.join((open(join('/', 'etc', 'issue'))).readlines())
    res = ''
    for s in raw:
        if s != '\\':
            res += s
        else:
            break
    while res.endswith(' '):
        res = res[:-1]

    return res