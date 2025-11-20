#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from myapp.models import Notificacao

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def notificar_tecnico(tecnico, titulo, mensagem, tipo="informacao", beneficiario=None):
    """
    Envia notificação para um técnico específico.
    
    Args:
        tecnico: Objeto User do técnico
        titulo: Título da notificação
        mensagem: Conteúdo da mensagem
        tipo: Tipo de notificação (atendimento_aguardando, urgente, informacao)
        beneficiario: Objeto Beneficiario (opcional)
    """
    
    # Registrar notificação no banco de dados
    notificacao = Notificacao.objects.create(
        usuario=tecnico,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,
        lida=False
    )
    
    if beneficiario:
        notificacao.beneficiario = beneficiario
        notificacao.save()
    
    # Enviar notificação em tempo real via WebSocket se o usuário estiver online
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"usuario_{tecnico.id}",
            {
                "type": "nova_notificacao",
                "notificacao_id": notificacao.id,
                "titulo": titulo,
                "mensagem": mensagem,
                "tipo": tipo,
                "beneficiario": beneficiario.nome_completo if beneficiario else None,
                "data_hora": notificacao.data_criacao.isoformat()
            }
        )
    except Exception as e:
        print(f"Erro ao enviar notificação WebSocket: {e}")

if __name__ == '__main__':
    main()