
from api_remote import utils


def proxy(request, backend_name, remote_path):
    """Retrieve url from a specific external backend"""

    backend = utils.load_backend(backend_name)
    rv = backend.get_url(remote_path, request)
    return rv
