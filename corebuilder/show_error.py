import sublime


def show_error(string):
    """
    Displays an error message with a standard "CoreBuilder" header

    :param string:
        The error to display
    """

    sublime.error_message(u'CoreBuilder\n\n%s' % string)
