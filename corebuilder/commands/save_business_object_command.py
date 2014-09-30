import os

import sublime
import sublime_plugin

from ..show_error import show_error
from ..download_authenticator import DownloadAuthenticator
from ..business_object_saver import BusinessObjectSaver

class SaveBusinessObjectCommand(sublime_plugin.WindowCommand, sublime_plugin.EventListener, BusinessObjectSaver):
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

    def on_post_save(self, view):
        settings = sublime.load_settings('CoreBuilder.sublime-settings')

        should_upload = view.settings().get('upload_on_save', settings.get('upload_on_save', True))

        filepath = view.file_name()
        filename = os.path.basename(filepath)
        filetype = os.path.splitext(filename)[1].lower()

        if not should_upload:
            # show_error('1')
            return
            
        if not filepath:
            # show_error('2')
            return
            
        if 'Packages\\User\\CoreBuilder.business-objects' not in filepath:
            # show_error('3')
            return

        if (not filetype == ".prg") and (not filetype == ".php"):
            # show_error('4')
            return

        view.settings().set('run_save', False)
        view.window().run_command('save_business_object')

    def run(self):
        auth = DownloadAuthenticator(self.window, self.on_done)
        auth.get_user_auth()

    def on_done(self):
        if not self.manager.settings.get('repository'):
           self.manager.__init__()
           
        should_save = self.window.active_view().settings().get('run_save', True)
        self.window.active_view().settings().set('run_save', True)

        filepath = self.window.active_view().file_name()
        filename = os.path.basename(filepath)
        filetype = os.path.splitext(filename)[1].lower()
        reference = os.path.splitext(filename)[0].upper()

        if not filepath:
            show_error(u'This business object file cannot be saved.')
            return False
            
        if 'Packages\\User\\CoreBuilder.business-objects' not in filepath:
            show_error(u"The business object can only be saved if it exists in the " + 
                u"\"Packages/User/CoreBuilder.business-objects\" folder, " +
                u"but seems to exist in \"%s\".\n\n" % filepath)
            return False

        if (not filetype == ".prg") and (not filetype == ".php"):
            show_error(u'Only \"prg\" and \"php\" business objects file types can be saved.')
            return False
        
        if should_save:
            self.window.active_view().run_command('save')

        self.on_save(reference, filepath, self.completed)

    def completed(self):
        if self.manager.last_error:
            show_error(self.manager.last_error)
            return False

        return True
