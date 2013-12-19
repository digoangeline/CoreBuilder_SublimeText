import os
import re
import threading

import sublime

from .thread_progress import ThreadProgress
from .business_object_manager import BusinessObjectManager


class BusinessObjectSaver():
    """
    Provides helper functionality related to save a business object
    """

    def __init__(self):
        self.manager = BusinessObjectManager()

    def on_save(self, reference, source_code):
        """
        Save business object handler

        :param picked:
            An integer of the business object index from the presented
            list. -1 means invalid.
        """

        thread = BusinessObjectSaverThread(self.manager, reference, source_code, None)
        thread.start()
        ThreadProgress(thread, 'Saving business object %s' % reference,
            'Business object %s successfully %s' % (reference, self.completion_type))


class BusinessObjectSaverThread(threading.Thread):
    """
    A thread to run business object operations in so that the main
    Sublime Text thread does not get blocked and freeze the UI
    """

    def __init__(self, manager, reference, source_code, on_complete):
        """
        :param manager:
            An instance of :class:`BusinessObjectManager`

        :param reference:
            The business object reference to save

        :param reference:
            The business object source code to save

        :param on_complete:
            A callback to run after saving the business object
        """

        self.reference = reference
        self.source_code = source_code
        self.manager = manager
        self.on_complete = on_complete
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.result = self.manager.save_business_object(self.reference, self.source_code)
        finally:
            if self.on_complete:
                sublime.set_timeout(self.on_complete, 1)
