"""Core code.

 INNER JOIN    LEFT JOIN     RIGHT JOIN    OUTER JOIN   SYMMETRIC JOIN
+---+--+---+  +---+--+---+  +---+--+---+  +---+--+---+   +---+--+---+
|   :**:   |  |***:**:   |  |   :**:***|  |***:**:***|   |***|  |***|
| L :**: R |  |*L*:**: R |  | L :**:*R*|  |*L*:**:*R*|   |*L*|  |*R*|
|   :**:   |  |***:**:   |  |   :**:***|  |***:**:***|   |***|  |***|
+---+--+---+  +---+--+---+  +---+--+---+  +---+--+---+   +---+--+---+

"""
from jsoncut.core import get_rootkey, select_key
from jsoncut.tokenizer import parse_keystr
from jsoncut.sequencer import Items

JOIN_FUNCTS = {
    'inner': lambda a, b: a & b,
    'left': lambda a, b: a,
    'right': lambda a, b: b,
    'outer': lambda a, b: a | b,
    'symmetric': lambda a, b: a ^ b
}


def join_data(d, keys, type_='inner'):
    """Join the two data sequences using the specified join type.

    Args:
        data (Item, Item): a 2d tuple of data sequences.
        keys (str, str): a 2d tuple of primary key lists used for join)
        jointype (str): 'inner', 'left', 'right', 'outer' or 'symmetric'.
    """
    values = tuple({select_key(k, *keys[i][0]): k for k in j.items}
                   for i, j in enumerate(d))
    keys = JOIN_FUNCTS[type_](set(values[0]), set(values[1]))
    if type_ == 'right':
        values = tuple(reversed(values))
    d[0].items = [{**values[0].get(i, {}), **values[1].get(i, {})}
                  for i in keys]
    return d[0].value


def join_(left, right, key, rgtkey=None, root=None, rgtroot=None,
          jointype='inner', fullscan=False, quotechar='"'):
    """The hub/core of JSON join.

    Args:
        data (obj, obj): a 2d tuple of JSON encodable objects.
        keys (str, str): a 2d tuple of primary keys used for join (JSON keys.)
        rootkeys (str, str): set the root of the object (JSON Key.)
        jointype (str): 'Inner', 'Left', 'Right', 'Outer' or 'Symmetric'.
        listkeys (bool): enumerated, sorted list all unique JSON Keys.
        inspect (bool): sorted list of all unique JSON Keys.
        fullpath (bool): used with get*; include the full key name path.
        fullscan (bool): don't skip previously visited JSON Keys.
        quotechar (str): the quote charcter used around JSON Keys.
    """
    quote = quotechar
    data = [left, right]
    keys = [key, key] if not rgtkey else [key, rgtkey]
    roots = ([root, root] if not rgtroot else [root, rgtroot])
    for i, d in enumerate(data):
        if roots[i]:
            keylist = parse_keystr(roots[i], data[i], quote, None, fullscan)
            data[i] = get_rootkey(data[i], *keylist[0])
        data[i] = Items(d)
        keys[i] = parse_keystr(keys[i], data[i].items, quote, None, fullscan)
    return join_data(data, keys, jointype)
