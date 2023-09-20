import uvicorn

from .settings import settings

uvicorn.run('api.app:app', reload=True, host=settings.server_host, port=settings.server_port,
            ssl_keyfile=settings.ssl_keyfile, ssl_certfile=settings.ssl_certfile, ssl_ca_certs=settings.ssl_ca_certs)

