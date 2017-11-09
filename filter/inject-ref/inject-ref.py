#!/usr/bin/env python3

from pandocinject import Injector
from pandocfilters import toJSONFilter
from importlib import import_module

if __name__ == "__main__":
    s = import_module('selector')
    f = import_module('formatter')
    i = Injector('inject-ref', selector_module=s, formatter_module=f)
    toJSONFilter(i.get_filter())

