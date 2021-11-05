import importlib
import logging
from itertools import chain
from typing import Callable

log = logging.getLogger(__name__)


def has_module(*modules, on_error: Callable = None, error_args=None):
    def inner():
        try:
            for name in modules:
                importlib.import_module(name)
        except ImportError:
            if error_args is not None:
                on_error(error_args)
            else:
                on_error()

            return False
        return True
    return inner


def find_files(*paths, pattern='*', recursive=True):
    return list(dict.fromkeys(chain(*[p.glob(f"{'**/' if recursive else ''}{pattern}") for p in paths])))
