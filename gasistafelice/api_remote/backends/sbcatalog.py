
from api_remote.backends import base

import json
import urllib2


class SBCatalogResourceBackend(base.ApiRemoteBackend):

    def get_data(self, full_url, as_string=False, del_from_cache=False):
        """Retrieve data from cache or from url, cache result, return data

        param:as_string set it to True if you want data to be returned as plaintext.
        """

        if del_from_cache:
            self.delete_from_cache(full_url)
            data = None
        else:
            data = self.get_from_cache(full_url)

        if not data:
            # Retrieve data
            result = urllib2.urlopen(full_url)
            data = result.read()
            self.save_in_cache(full_url, data)

        if not as_string:
            data = json.loads(data)

        return data
