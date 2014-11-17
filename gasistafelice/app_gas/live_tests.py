
from django.test.utils import setup_test_environment
setup_test_environment()

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from pprint import pprint
import json, sys

client = Client()

def _do_get(url):
    response = client.get(url)
    print("RESPONSE: ", response.content)
    print("STATUS_CODE: ", response.status_code)
    print("RESPONSE __dict__: ")
    pprint(response.__dict__)
    return response

def _get_block(resource_type, resource_id, view_type, *args):

    kw = { 
        'resource_type' : resource_type,
        'resource_id' : resource_id,
        'view_type' : view_type,
    }
    view_name = 'get-block'
    if args:
        view_name = 'get-block-with-args'
        kw['args'] = "/".join(args)

    url = reverse(view_name, kwargs=kw)
    response = _do_get(url)
    return response

def test_block_balance_pact(*args):

    # http://gasistafelice.befair.it:9001/gasistafelice/rest/pact/5/balance_pact/

    try:
        resource_id = args[0]
    except IndexError:
        resource_id = 1

    response = _get_block(
        resource_type = "pact",
        resource_id = resource_id,
        view_type = "balance_pact"
    )
    
def authenticate(username, passwd):
    client.login(username=username, password=passwd)

def testalo(url, username, passwd, test_fun, *test_args):

    authenticate(username, passwd)
    test_fun(*test_args)

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Prova con %s <http site base> <username> <password> <test_name> [args... to test function]")
        sys.exit(100)

    base_url = sys.argv[1]
    username = sys.argv[2]
    passwd = sys.argv[3]
    test_fun = locals()[sys.argv[4]]
    args = sys.argv[5:]

    testalo(base_url, username, passwd, test_fun, *args)



#--- APPUNTI LF ---#

def test_dummy():
    response = client.get('/')
    print response.status_code

    response = client.get(reverse('interpolator_home'))
    print("RESPONSE: ", response.content)
    print("STATUS_CODE: ", response.status_code)

    #NOTE LF: response = client.post(
    #NOTE LF:     url, content_type='application/json',
    #NOTE LF:     data=json.dumps(body)
    #NOTE LF: )

