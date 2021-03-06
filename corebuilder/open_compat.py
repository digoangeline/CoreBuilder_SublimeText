import os
import sys
import re

from .file_not_found_error import FileNotFoundError


def open_compat(path, mode='r'):
    if mode in ['r', 'rb'] and not os.path.exists(path):
        raise FileNotFoundError(u"The file \"%s\" could not be found" % path)

    if sys.version_info >= (3,):
        encoding = 'utf-8'
        errors = 'replace'
        if mode in ['rb', 'wb', 'ab']:
            encoding = None
            errors = None
        return open(path, mode, encoding=encoding, errors=errors)

    else:
        return open(path, mode)


def read_compat(file_obj):
    if sys.version_info >= (3,):
        return file_obj.read()
    else:
        return unicode(file_obj.read(), 'utf-8', errors='replace')


def fix_windows_path(file):
    if os.name == 'nt':
        file = file.replace('\\', '/')
        file = re.sub('^([A-Za-z]):', '/\\1', file)
        file = file[0:2].upper() + file[2:]
    return file

