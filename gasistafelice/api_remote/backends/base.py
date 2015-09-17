
from django.http import HttpResponse

# from lib.cache import Store as _cache

import time
import urlparse


class ApiRemoteBackend(object):

    def __init__(self, settings_dict):
        super(ApiRemoteBackend, self).__init__()
        self.settings_dict = settings_dict
        self.base_url = urlparse.urlunsplit((
            settings_dict['PROTOCOL'],
            "%s:%s" % (settings_dict['HOST'], settings_dict['PORT']),
            settings_dict['BASE_PATH'],
            '', ''
        ),)
        self.username = self.settings_dict['USER']
        self.password = self.settings_dict['PASSWORD']

    def get_url(self, url, request):
        """Retrieve an url, return http response.

        Take as input the original request as the backend
        should pass also GET or POST parameters and
        could do some considerations basing on other settings
        of the request itself.
        """

        full_url = self.base_url + url
        qs = request.META['QUERY_STRING']
        if qs:
            full_url += "?" + qs
        data = self.get_data(full_url, as_string=True)
        return HttpResponse(data, content_type="application/json")

    def get_remote_info(self, resource):
        """Dispatcher to real getter method for specific resource type.

        Default machinery calls get_<resource_type>_info method
        """

        try:
            method_name = "get_%s_info" % resource.ext_res_type
        except KeyError:
            raise NotImplementedError(
                "Backend %s method to retrieve remote info for a %s" % (
                    self.__class__.__name__, resource.ext_res_type))

        return getattr(self, method_name)(resource)

    def get_from_cache(self, full_url):
        pass

    def delete_from_cache(self, full_url):
        pass

    def save_in_cache(self, full_url, data):
        pass

    def get_data(self, full_url, as_string=False, del_from_cache=False):
        raise NotImplementedError("to be implemented in subclasses")

#class CachedResourceBackend(ApiRemoteBackend):
#
#    CACHE_REFRESH_INTERVAL = 10000
#
#    def get_from_cache(self, full_url):
#
#        key = self.cache_key(full_url)
#        cached_entry = _cache.get(key)
#        rv = None
#        if cached_entry:
#            if self.cached_entry_is_valid(cached_entry):
#                rv = cached_entry['data']
#
#        return rv
#
#    def save_in_cache(self, full_url, data):
#
#        key = self.cache_key(full_url)
#        _cache.set(key, {
#            'timestamp': int(time.time()),
#            'data': data
#        })
#        return True
#
#    def delete_from_cache(self, full_url):
#
#        key = self.cache_key(full_url)
#        # COMMENT Matteo: exception here should be handled from
#        # redis
#        _cache.delete(key)
#        return True
#
#    @classmethod
#    def cache_key(cls, url):
#        return url
#        # return "%s-%s" % (cls.__name__.lower(), url)
#
#    def cached_entry_is_valid(self, cached_entry):
#
#        timestamp = cached_entry['timestamp']
#        return int(time.time()) - timestamp < self.CACHE_REFRESH_INTERVAL
#
#    def clean_cache(self):
#        _cache.clean()


# class FBResourceBackend(ApiRemoteBackend):
#
#    def get_auth_querystring(self):
#        # Use OpenAction access token to build querystring (see: social auth)
#        return "TODO"
#
#    def do_request(self, destination):
#        """Given a destination (usually a URL), manage authentication if needed."""
#
#        url = destination
#        url += "&%s" % self.get_auth_querystring()
#        response = urllib2.open(url)
#        raw_data = response.read()
#        return raw_data
#
#    def get_user_info(self, resource):
#        """Call Facebook API and return normalized data."""
#
#        fields = ['id','name','email', 'username']
#        auth_qs = self.get_auth_querystring()
#
#        graphapi_url = "https://graph.facebook.com/%s?fields=%s&format=json&%s" % (self.id, ",".join(fields), auth_qs)
#
#        raw_data = self.do_request(graphapi_url)
#        data = json.load(raw_data)
#
#        normalized_data = {
#            'id': data.get('id'),
#            'name': data.get('name'),
#            'email': data.get('email'),
#            'username': data.get('username'),
#        }
#
#        return normalized_data
