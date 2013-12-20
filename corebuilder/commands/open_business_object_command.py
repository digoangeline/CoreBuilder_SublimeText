import threading

import sublime
import sublime_plugin

from ..show_error import show_error
from ..download_authenticator import DownloadAuthenticator
from ..business_object_manager import BusinessObjectManager
from ..thread_progress import ThreadProgress

class OpenBusinessObjectCommand(sublime_plugin.WindowCommand):
    """
    A command that opens a business object.
    """

    def __init__(self, window):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the available business object list in.
        """

        self.window = window
        self.completion_type = 'opened'

    def run(self):
        auth = DownloadAuthenticator(self.window, self.on_done)
        auth.get_user_auth()
        
    def on_done(self):
        ref_object = ''
        for region in self.window.active_view().sel():
            ref_object = ref_object + self.window.active_view().substr(region)
        if ref_object:
            thread = OpenBusinessObjectThread(self.window, ref_object, None)
            thread.start()
            ThreadProgress(thread, 'Opening business object %s' % ref_object,
                'Business object %s successfully %s' % (ref_object, self.completion_type))

    def is_enabled(self):
        text = ''
        for region in self.window.active_view().sel():
            text = text + self.window.active_view().substr(region)
        if not text:
            return False
        return True


class OpenBusinessObjectThread(threading.Thread, BusinessObjectManager):
    """
    A thread to run the action of opening a business objects.
    """

    def __init__(self, window, ref_object, on_complete):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the available business object list in.
        """

        self.window = window
        self.ref_object = ref_object
        self.on_complete = on_complete
        threading.Thread.__init__(self)
        BusinessObjectManager.__init__(self)

    def run(self):
        if not self.settings.get('repository'):
            self.__init__(self.window, self.ref_object, self.on_complete)

        try:
            self.result = self.open_business_object(self.ref_object, True)
        finally:
            if self.on_complete:
                sublime.set_timeout(self.on_complete, 1)
