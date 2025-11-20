"""
ASGI config for cras360 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

application = get_asgi_application()

# Esta é uma configuração básica de ASGI
# Para WebSockets completos, seria necessário instalar e configurar o pacote Django Channels
# E adicionar código como:
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import apps.notificacoes.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             apps.notificacoes.routing.websocket_urlpatterns
#         )
#     ),
# })
