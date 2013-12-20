import os

import sublime
import sublime_plugin

from ..show_error import show_error
from ..download_authenticator import DownloadAuthenticator
from ..business_object_saver import BusinessObjectSaver


class SaveBusinessObjectCommand(sublime_plugin.WindowCommand, BusinessObjectSaver):
    """
    A command that uploads a business object to the CoreBuilder Server.
    """

    def __init__(self, window=sublime.active_window()):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the business object.
        """

        self.window = window
        self.completion_type = 'saved'
        BusinessObjectSaver.__init__(self)

    def run(self):
        auth = DownloadAuthenticator(self.window, self.on_done)
        auth.get_user_auth()

    def on_done(self):
        def save():
            filepath = self.window.active_view().file_name()
            if not filepath:
                show_error(u'This business object file cannot be saved.')
                return False
            if 'Packages\\User\\CoreBuilder.business-objects' not in filepath:
                show_error(u"The business object can only be saved if it exists in the " + 
                    u"\"Packages/User/CoreBuilder.business-objects\" folder, " +
                    u"but seems to exist in \"%s\".\n\n" % filepath)
                return False

            filename = os.path.basename(filepath)
            filetype = os.path.splitext(filename)[1].lower()
            if (not filetype == ".prg") and (not filetype == ".php"):
                show_error(u'Only \"prg\" and \"php\" business objects file types can be saved.')
                return False

            reference = os.path.splitext(filename)[0].upper()
            self.on_save(reference, filepath)
            return True
        sublime.set_timeout(save, 10)
