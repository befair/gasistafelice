EXTERNAL_API_BACKENDS = {
    "sbcatalog": {
        'ENGINE': "api_remote.backends.sbcatalog.SBCatalogResourceBackend",
        'HOST': 'sbcatalog.labs.befair.it',
        'PORT': 80,
        'PROTOCOL': 'http',
        'BASE_PATH': '/api/',
        'USER': 'your_user_here',
        'PASSWORD': 'your_password_here',
    },
}

# Redis cache server

# IP:PORT address. None will use default values
REDIS_SERVER_ADDR = None
REDIS_SERVER_PORT = None

# Redis Database identifier. None will use default values
REDIS_DATABASE = None
