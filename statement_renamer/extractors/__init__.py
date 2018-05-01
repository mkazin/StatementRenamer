from .extractor import DateExtractor
from importlib import import_module
import pkgutil
import os
import sys

"""
Auto-import of all classes extending the DateExtractor Base Class, 
allowing the ExtractorFactory to use __subclasses__ to iterate over them,
while leaving them loosely coupled.

Many thanks to Luna for the walk-through in:
https://www.bnmetrics.com/blog/factory-pattern-in-python3-simple-version
"""

for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):

    try:
        imported_module = import_module('.' + name, package=__package__)

        class_name = list(filter(lambda x: x != 'DateExtractor' and not x.startswith('__'),
                                 dir(imported_module)))

        extractor_class = getattr(imported_module, class_name[0])

        if issubclass(extractor_class, DateExtractor):
            setattr(sys.modules[__name__], name, extractor_class)

    except ImportError as e:
        # TODO: LOG an error
        print("LOG an error", e)
