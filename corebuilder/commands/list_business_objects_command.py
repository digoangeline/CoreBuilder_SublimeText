import threading

import sublime
import sublime_plugin

from ..show_error import show_error
from ..download_authenticator import DownloadAuthenticator
from ..business_object_opener import BusinessObjectOpener
from ..thread_progress import ThreadProgress

class ListBusinessObjectsCommand(sublime_plugin.WindowCommand):
    """
    A command that presents the list of available business objects and allows the
    user to pick one to open.
    """

    def run(self):
        auth = DownloadAuthenticator(self.window, self.on_done)
        auth.get_user_auth()
        
    def on_done(self):
        thread = ListBusinessObjectsThread(self.window)
        thread.start()
        ThreadProgress(thread, 'Loading business objects', '')


class ListBusinessObjectsThread(threading.Thread, BusinessObjectOpener):
    """
    A thread to run the action of retrieving available business objects in. Uses the
    default BusinessObjectOpener.on_done quick panel handler.
    """

    def __init__(self, window):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the available business object list in.
        """

        self.window = window
        self.completion_type = 'opened'
        threading.Thread.__init__(self)
        BusinessObjectOpener.__init__(self)

    def run(self):
        if not self.manager.settings.get('repository'):
            self.manager.__init__()

        self.business_object_list = self.make_business_object_list()

        if self.manager.last_error:
            show_error(self.manager.last_error)
            return

        def show_quick_panel():
            if not self.business_object_list:
                show_error('There are no business objects available. Please view the console for more details.')
                return
            self.window.show_quick_panel(self.business_object_list, self.on_done)
        sublime.set_timeout(show_quick_panel, 10)
