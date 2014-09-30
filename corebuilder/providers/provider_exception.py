import sublime

from ..download_authenticator import DownloadAuthenticator

class ProviderException(Exception):
    """If a provider could not return information"""

    def __str__(self):
        auth = DownloadAuthenticator()
        auth.clear_user_auth()
        return self.args[0]
