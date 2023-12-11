from rmbserver.servers.base import app
from rmbserver.servers.datasource import ns_datasource
from rmbserver.servers.chat import ns_chat
from rmbserver.servers.test import ns_test
from rmbserver.servers.exception_handler import *


def run_server():
    app.run('0.0.0.0', 5000)


__ALL__ = [
    'run_server',
    'app',
    'ns_datasource',
    'ns_chat',
    'ns_test'
]
