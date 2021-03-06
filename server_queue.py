import fix_path  # noqa

import json
import logging

from google.appengine.api import taskqueue

import gce

START_EVENT = 'START_SERVER'
STOP_EVENT = 'STOP_SERVER'
BACKUP_EVENT = 'BACKUP_SERVER'
RESTART_EVENT = 'RESTART_SERVER'


def queue_controller_task(payload):
    payload = json.dumps(payload)
    taskqueue.Queue('controller').add([taskqueue.Task(payload=payload, method='PULL')])


def start_server(server, reserved_ports=None):
    try:
        instance = gce.Instance.singleton()
        instance.start()
        if instance.idle:
            instance.idle = None
            instance.put()
        payload = {'event': START_EVENT}
        payload['server_key'] = server.key.urlsafe()
        payload['agent_client_id'] = server.agent.client_id
        payload['agent_secret'] = server.agent.secret
        payload['minecraft_url'] = server.minecraft_url
        payload['memory'] = server.memory
        payload['reserved_ports'] = reserved_ports or list()
        payload['server_properties'] = server.mc_properties.server_properties
        operator = server.operator
        if operator is not None:
            payload['operator'] = operator
        queue_controller_task(payload)
    except Exception as e:
        logging.exception(e)
        raise


def backup_server(server):
    try:
        payload = {'event': BACKUP_EVENT}
        payload['server_key'] = server.key.urlsafe()
        queue_controller_task(payload)
    except Exception as e:
        logging.exception(e)
        raise


def restart_server(server):
    try:
        payload = {'event': RESTART_EVENT}
        payload['server_key'] = server.key.urlsafe()
        queue_controller_task(payload)
    except Exception as e:
        logging.exception(e)
        raise


def stop_server(server):
    try:
        payload = {'event': STOP_EVENT}
        payload['server_key'] = server.key.urlsafe()
        queue_controller_task(payload)
    except Exception as e:
        logging.exception(e)
        raise
