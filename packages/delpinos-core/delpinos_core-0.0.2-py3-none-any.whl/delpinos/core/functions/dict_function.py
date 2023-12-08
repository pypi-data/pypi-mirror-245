# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

from typing import Any, Dict


def dict_merge(
    dct: Dict[str, Any],
    merge_dct: Dict[str, Any],
    add_keys: bool = True,
) -> Dict[str, Any]:
    """Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    This version will return a copy of the dictionary and leave the original
    arguments untouched.

    The optional argument ``add_keys``, determines whether keys which are
    present in ``merge_dict`` but not ``dct`` should be included in the
    new dict.

    Args:
        dct (dict) onto which the merge is executed
        merge_dct (dict): dct merged into dct
        add_keys (bool): whether to add new keys

    Returns:
        dict: updated dict
    """

    dct = dct.copy() if isinstance(dct, dict) else {}
    merge_dct = merge_dct if isinstance(merge_dct, dict) else {}

    if not add_keys:
        try:
            merge_dct = {k: merge_dct[k] for k in set(dct).intersection(set(merge_dct))}
        except Exception:
            return dct

    for k in merge_dct:
        try:
            if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict):
                dct[k] = dict_merge(dct[k], merge_dct[k], add_keys=add_keys)
            else:
                dct[k] = merge_dct[k]
        except Exception:
            return dct

    return dct


def dicts_merge(*args) -> Dict[str, Any]:
    dct = {}
    for merge_dct in args:
        dct = dict_merge(dct, merge_dct, add_keys=True)
    return dct
