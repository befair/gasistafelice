#!/usr/bin/env python2

import Cookie
import cookielib
import collections
import sys
import urllib
import urllib2
from os.path import realpath

LEGACY_REST_PREFIX = "gasistafelice/rest/"
verbose = False


def get_cookie(base_url):
    """ Init the session with the backend and return the session cookie """

    auth_url = base_url + \
        "gasistafelice/accounts/login/?next=/gasistafelice/rest"
    req = urllib2.Request(auth_url)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.open(req)

    for cookie in cj:
        if cookie.name == "csrftoken":
            csrftoken = cookie.value
        elif cookie.name == "sessionid":
            sessionid = cookie.value

    data = urllib.urlencode({"username": "01gas1",
                             "password": "des",
                             "csrfmiddlewaretoken": csrftoken})
    c = Cookie.SimpleCookie()
    c['sessionid'] = sessionid
    c['csrftoken'] = csrftoken
    cookie_string = c.output(header="", sep=";")

    urllib2.Request(auth_url, data=data, headers={"Cookie": cookie_string})
    return c


def check_url(cookie, url):
    """
    Check that a url returns HTTP status code 200
    """

    # Selenium does not offer a way to check the HTTP status code,
    # and it would even slow to use it for this kind of tests,
    # so we get the valid session id from the webdriver and we pass
    # it in the cookie header
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    cookie_string = cookie.output(header="", sep=";")

    headers = {'User-Agent': user_agent, 'Cookie': cookie_string, }

    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    return resp


def main(base_url):
    """
    Do the job and return a dictionary with elements:
    * 'OK' => a list of dicts with 'code' and 'url' of success;
    * 'ERROR' => a list of dicts with 'code' and 'url' of failures;
    The urls are readed from the "urls.txt" failures
    """

    cookie = get_cookie(base_url)
    rv = collections.OrderedDict([('OK', []), ('ERROR', [])])

    # get the script directory, that is the same of "urls.txt"
    file_dir = '/'.join(realpath(__file__).split('/')[:-1])
    with open(file_dir + "/urls.txt", "r") as urls_file:
        for line in urls_file.readlines():
            # strip the '/n'
            url = base_url + line[:-1]
            try:
                response = check_url(cookie, url)
            except urllib2.HTTPError, e:
                rv['ERROR'].append({'code': e.code, 'url': url})
            else:
                rv['OK'].append({'code': response.getcode(), 'url': url})

    return rv


def test_entrypoint():
    """Entrypoint for pytest runner"""
    base_url = "http://localhost:8080/"

    if __name__ == "__main__":
        try:
            base_url = sys.argv[1]
        except IndexError:
            pass

    rv = main(base_url)
    for kind, resps in rv.items():
        for r in resps:
            formatted_out = "{}[{}] {}".format(kind, r['code'], r['url'])
            if verbose:
                print(formatted_out)
            assert r['code'] == 200, formatted_out


if __name__ == "__main__":
    verbose = True
    test_entrypoint()
