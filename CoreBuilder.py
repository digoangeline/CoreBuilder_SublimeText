import sublime
import sys
import os


st_version = 2

# Warn about out-dated versions of ST3
if sublime.version() == '':
    st_version = 3
    print('CoreBuilder: Please upgrade to Sublime Text 3 build 3012 or newer')

elif int(sublime.version()) > 3000:
    st_version = 3


if st_version == 3:
    installed_dir, _ = __name__.split('.')
elif st_version == 2:
    installed_dir = os.path.basename(os.getcwd())


# Ensure the user has installed CoreBuilder properly
if installed_dir != 'CoreBuilder':
    message = (u"CoreBuilder\n\nThis package appears to be installed " +
        u"incorrectly.\n\nIt should be installed as \"CoreBuilder\", " +
        u"but seems to be installed as \"%s\".\n\n" % installed_dir)
    sublime.error_message(message)

# Normal execution will finish setting up the package
else:
    reloader_name = 'corebuilder.reloader'

    # ST3 loads each package as a module, so it needs an extra prefix
    if st_version == 3:
        reloader_name = 'CoreBuilder.' + reloader_name
        from imp import reload

    # Make sure all dependencies are reloaded on upgrade
    if reloader_name in sys.modules:
        reload(sys.modules[reloader_name])


    try:
        # Python 3
        from .corebuilder import reloader

        from .corebuilder.commands import *

    except (ValueError):
        # Python 2
        from corebuilder import reloader
        from corebuilder import sys_path

        from corebuilder.commands import *


    def plugin_loaded():
        # Make sure the user's locale can handle non-ASCII. A whole bunch of
        # work was done to try and make CoreBuilder work even if the locale
        # was poorly set, by manually encoding all file paths, but it ended up
        # being a fool's errand since the package loading code built into
        # Sublime Text is not written to work that way, and although packages
        # could be installed, they could not be loaded properly.
        try:
            os.path.exists(os.path.join(sublime.packages_path(), u"fran\u00e7ais"))
        except (UnicodeEncodeError) as e:
            message = (u"CoreBuilder\n\nYour system's locale is set to a " +
                u"value that can not handle non-ASCII characters. CoreBuilder " +
                u"can not properly work unless this is fixed.\n\n" +
                u"On Linux, please reference your distribution's docs for " +
                u"information on properly setting the LANG environmental " +
                u"variable. As a temporary work-around, you can launch " +
                u"Sublime Text from the terminal with:\n\n" +
                u"LANG=en_US.UTF-8 sublime_text")
            sublime.error_message(message)
            return

    if st_version == 2:
        plugin_loaded()
