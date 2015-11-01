#!/usr/bin/env python2

import Cookie
import urllib2
import sys
from selenium import webdriver
from gf.settings import RESOURCE_PAGE_BLOCKS
import collections

LEGACY_REST_PREFIX = "gasistafelice/rest/"

def get_default_check_rel_paths():
    rel_paths = []
    for resource, tabs in RESOURCE_PAGE_BLOCKS.items():
        rel_paths.append("{}/1/".format(resource))
        for tab in tabs:
            rel_paths += [
                "{}/1/{}".format(resource, block_name) for block_name in tab['blocks']]
    return rel_paths

def init_gf_connection(base_url):
    browser = webdriver.PhantomJS()
    # Login
    browser.get(base_url + '/gasistafelice/accounts/login/?next=/gasistafelice/rest/')
    el = browser.find_element_by_id("id_username")
    el.send_keys("01gas1")
    el = browser.find_element_by_id("id_password")
    el.send_keys("des")
    el = browser.find_element_by_css_selector("input[type=submit]")
    el.click()
    return browser

def check_url(browser, url):
    """
    Check that a url returns HTTP status code 200
    """

    # Selenium does not offer a way to check the HTTP status code,
    # and it would even slow to use it for this kind of tests,
    # so we get the valid session id from the webdriver and we pass
    # it in the cookie header
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    cookie = Cookie.SimpleCookie()
    cookie["sessionid"] = browser.get_cookie('sessionid')['value']
    cookie_string = cookie.output(header="", sep=";")

    headers = {
        'User-Agent' : user_agent,
        'Cookie' : cookie_string,
    }

    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    return resp

def iterpaths(rel_paths):
    """
    Combine urls with relative paths in a single list
    """
    for rel_path in rel_paths:
        yield LEGACY_REST_PREFIX + rel_path

def main(base_url, rel_paths):
    """
    Do the job and return a dictionary with elements:
    * 'OK' => a list of dicts with 'code' and 'url' of success;
    * 'ERROR' => a list of dicts with 'code' and 'url' of failures;
    """

    browser = init_gf_connection(base_url)
    rv = collections.OrderedDict([('OK',[]),('ERROR',[])])

    for path in iterpaths(rel_paths):
        url = base_url + '/' + path
        try:
            response = check_url(browser, url)
        except urllib2.HTTPError, e:
            rv['ERROR'].append({'code': e.code, 'url': url})
        else:
            rv['OK'].append({'code': response.getcode(), 'url': url})

    return rv

if __name__ == "__main__":

    try:
        base_url = sys.argv[1]
    except IndexError:
        base_url = "http://localhost:8080/"

    try:
        rel_paths = sys.argv[2].split(",")
    except IndexError:
        rel_paths = get_default_check_rel_paths()

    rv = main(base_url, rel_paths)
    for kind, resps in rv.items():
        for r in resps:
            print("{}[{}] {}".format(kind, r['code'], r['url']))

    sys.exit(0) if not rv['ERROR'] else sys.exit(100)
