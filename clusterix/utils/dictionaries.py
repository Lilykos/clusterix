def flatten_dict(dictionary, l_key='', separator=':'):
    """
    Flattens a dictionary using a specified separator to provide an XPath-like
    data structure. The flattening happens up to the first level of lists.

    :param dictionary: The dict to be flattened.
    :type dictionary: dict

    :param l_key: The left key used for flattening (not to be used externally).
    :type l_key: str

    :param separator: The separator for the flattened keys.
    :type separator: str

    :return: A flattened dictionary (up to the first level, lists are not flattened).
    :rtype: dict
    """
    flat = {}
    for r_key, val in dictionary.items():
        key = l_key + r_key

        # If it is a dict, recursion to flatten it
        if isinstance(val, dict):
            flat.update(flatten_dict(val, l_key=key+separator))
        else:
            flat[key] = val
    return flat