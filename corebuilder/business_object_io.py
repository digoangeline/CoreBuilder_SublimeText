import os

import sublime

from .console_write import console_write
from .open_compat import open_compat, read_compat
from .unicode import unicode_from_os
from .file_not_found_error import FileNotFoundError


def read_business_object_file(business_object, relative_path, binary=False, debug=False):
    business_object_dir = _get_business_object_dir(business_object)
    file_path = os.path.join(business_object_dir, relative_path)

    if os.path.exists(business_object_dir):
        result = _read_regular_file(business_object, relative_path, binary, debug)
        if result != False:
            return result

    if debug:
        console_write(u"Unable to find file %s in the business object %s" % (relative_path, business_object), True)
    return False


def business_object_file_exists(business_object, relative_path):
    business_object_dir = _get_business_object_dir(business_object)
    file_path = os.path.join(business_object_dir, relative_path)

    if os.path.exists(business_object_dir):
        result = _regular_file_exists(business_object, relative_path)
        if result:
            return result

    return False


def _get_business_object_dir(business_object):
    """:return: The full filesystem path to the business object directory"""

    return os.path.join(sublime.packages_path(), business_object)


def _read_regular_file(business_object, relative_path, binary=False, debug=False):
    business_object_dir = _get_business_object_dir(business_object)
    file_path = os.path.join(business_object_dir, relative_path)
    try:
        with open_compat(file_path, ('rb' if binary else 'r')) as f:
            return read_compat(f)

    except (FileNotFoundError) as e:
        if debug:
            console_write(u"Unable to find file %s in the business object folder for %s" % (relative_path, business_object), True)
        return False


def _regular_file_exists(business_object, relative_path):
    business_object_dir = _get_business_object_dir(business_object)
    file_path = os.path.join(business_object_dir, relative_path)
    return os.path.exists(file_path)
