import sublime

from ..download_authenticator import DownloadAuthenticator

class DownloaderException(Exception):
    """If a downloader could not download a URL"""

    def __str__(self):
        auth = DownloadAuthenticator()
        auth.clear_user_auth()
        return self.args[0]