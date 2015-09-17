
from api_remote import settings
from lib import load_symbol


def load_backend(backend_name):
    """Retrieve settings, load class and instantiate backend passing settings_dict"""
    backend_settings = settings.EXTERNAL_API_BACKENDS[backend_name]
    backend_class_path = backend_settings['ENGINE']
    backend_class = load_symbol(backend_class_path)
    return backend_class(backend_settings)
