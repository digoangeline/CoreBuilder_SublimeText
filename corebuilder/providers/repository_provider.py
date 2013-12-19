import json
import re
import os
from itertools import chain

try:
    # Python 3
    from urllib.parse import urlparse
except (ImportError):
    # Python 2
    from urlparse import urlparse

from ..console_write import console_write
from .provider_exception import ProviderException
from ..downloaders.downloader_exception import DownloaderException
from ..clients.client_exception import ClientException
from ..download_manager import downloader


class RepositoryProvider():
    """
    Generic repository downloader that fetches business object info

    The structure of the JSON a repository should contain is located in
    example-business-objects.json.

    :param repo:
        The URL of the business object repository

    :param settings:
        A dict containing at least the following fields:
          `debug`,
          `timeout`,
          `user_agent`,
          `user_name`,
          `user_pass`
        Optional fields:
          `http_proxy`
          `https_proxy`,
          `proxy_username`,
          `proxy_password`
    """

    def __init__(self, repo, settings):
        self.repo_info = None
        self.repo = repo
        self.settings = settings
        self.failed_sources = {}

    @classmethod
    def match_url(cls, repo):
        """Indicates if this provider can handle the provided repo"""

        return True

    def prefetch(self):
        """
        Go out and perform HTTP operations, caching the result

        :raises:
            DownloaderException: when there is an issue download business object info
            ClientException: when there is an issue parsing business object info
        """

        self.fetch()

    def get_failed_sources(self):
        """
        List of any URLs that could not be accessed while accessing this repository

        :return:
            A generator of ("https://example.com", Exception()) tuples
        """

        return self.failed_sources.items()

    def fetch(self):
        """
        Retrieves and loads the JSON for other methods to use

        :raises:
            ProviderException: when an error occurs trying to open a file
            DownloaderException: when an error occurs trying to open a URL
        """

        if self.repo_info != None:
            return

        self.repo_info = self.fetch_location(self.repo)

    def fetch_location(self, location):
        """
        Fetches the contents of a URL of file path

        :param location:
            The URL or file path

        :raises:
            ProviderException: when an error occurs trying to open a file
            DownloaderException: when an error occurs trying to open a URL

        :return:
            A dict of the parsed JSON
        """

        if re.match('https?://', self.repo, re.I):
            with downloader(location, self.settings) as manager:
                json_string = manager.fetch(location, 'Error downloading repository.')

        # Anything that is not a URL is expected to be a filesystem path
        else:
            if not os.path.exists(location):
                raise ProviderException(u'Error, file %s does not exist' % location)

            if self.settings.get('debug'):
                console_write(u'Loading %s as a repository' % location, True)

            # We open as binary so we get bytes like the DownloadManager
            with open(location, 'rb') as f:
                json_string = f.read()

        try:
            return json.loads(json_string.decode('utf-8'))
        except (ValueError):
            raise ProviderException(u'Error parsing JSON from repository %s.' % location)

    def get_business_objects(self):
        """
        Provides access to the business objects in this repository

        :raises:
            ProviderException: when an error occurs trying to open a file
            DownloaderException: when there is an issue download business object info
            ClientException: when there is an issue parsing business object info

        :return:
            A generator of
            (
                'Business Object Reference',
                {
                    'reference': reference,
                    'description': description,
                    'version': version,
                    'url': url
                }
            )
        """

        self.fetch()

        def fail(message):
            exception = ProviderException(message)
            self.failed_sources[self.repo] = exception
            return
        
        if 'error' in self.repo_info:
            error_string = "Unable to list business objects from {0}. The following error message has returned: {1}".format(self.repo, self.repo_info['error'].encode('utf-8'))
            fail(error_string)
            return

        schema_error = u'Repository %s does not appear to be a valid repository file because' % self.repo
        if 'business_objects' not in self.repo_info:
            error_string = u'%s the "business_objects" JSON key is missing.' % schema_error
            fail(error_string)
            return

        output = {}
        for business_object in self.repo_info['business_objects']:
            info = {
                'source': self.repo
            }

            for field in ['reference', 'description', 'version', 'url']:
                if business_object.get(field):
                    info[field] = business_object.get(field)

            output[info['reference']] = info

        return output
