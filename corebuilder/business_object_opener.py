import os
import re
import threading

import sublime

from .thread_progress import ThreadProgress
from .business_object_manager import BusinessObjectManager


class BusinessObjectOpener():
    """
    Provides helper functionality related to open a business object
    """

    def __init__(self):
        self.manager = BusinessObjectManager()

    def make_business_object_list(self, ignore_business_objects=[]):
        """
        Creates a list of business objects and what operation would be performed for
        each. Returns the information in a format suitable for displaying in the
        quick panel.

        :param ignore_business_objects:
            A list of business objects references that should not be returned in the list

        :return:
            A list containing three strings:
              0 - business object reference
              1 - business object description
              2 - business object version
        """

        business_objects = self.manager.list_available_business_objects()

        business_object_list = []
        for business_object in sorted(iter(business_objects.keys()), key=lambda s: s.lower()):
            business_object_entry = [business_object]
            info = business_objects[business_object]

            description = info.get('description')
            if not description:
                description = '<No description provided>'
            business_object_entry.append(description)
            
            version = info.get('version')
            if not version:
                version = '<No version provided>'
            business_object_entry.append(version)

            business_object_list.append(business_object_entry)

        return business_object_list


    def on_done(self, picked):
        """
        Quick panel user selection handler - open a business object

        :param picked:
            An integer of the business object index from the presented
            list. -1 means invalid.
        """

        if picked == -1:
            return
        reference = self.business_object_list[picked][0]

        thread = BusinessObjectOpenerThread(self.manager, reference, None)
        thread.start()
        ThreadProgress(thread, 'Openning business object %s' % reference,
            'Business object %s successfully %s' % (reference, self.completion_type))


class BusinessObjectOpenerThread(threading.Thread):
    """
    A thread to run business object operations in so that the main
    Sublime Text thread does not get blocked and freeze the UI
    """

    def __init__(self, manager, reference, on_complete):
        """
        :param manager:
            An instance of :class:`BusinessObjectManager`

        :param reference:
            The business object reference to open

        :param on_complete:
            A callback to run after openning the business object
        """

        self.reference = reference
        self.manager = manager
        self.on_complete = on_complete
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.result = self.manager.open_business_object(self.reference)
        finally:
            if self.on_complete:
                sublime.set_timeout(self.on_complete, 1)
