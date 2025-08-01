import os
import sys
import json
from datetime import datetime

# Configurações básicas do Gunicorn
bind = "0.0.0.0:" + str(os.getenv("PORT", "8000"))
workers = int(os.getenv("WEB_CONCURRENCY", "4"))
worker_class = "gthread"
threads = int(os.getenv("MAX_THREADS", "2"))
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = int(os.getenv("KEEPALIVE", "5"))

# Configurações de performance
max_requests = int(os.getenv("MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", "50"))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "30"))

# Configurações de segurança
forwarded_allow_ips = os.getenv("FORWARDED_ALLOW_IPS", "127.0.0.1,::1")
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on',
    'X-FORWARDED-HOST': 'hoztech.com.br'
}

# Configurações de log
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")

# Logger simplificado para o Railway
class RailwayLogger:
    def __init__(self, app):
        self.app = app
        self.error_log = sys.stderr
        self.access_log = sys.stdout
        self.loglevel = loglevel
        self.access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

    def _log(self, level, msg, *args, **kwargs):
        log_entry = {
            'severity': level,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'message': msg % args if args else msg,
            'service': 'hoztechsite'
        }
        print(json.dumps(log_entry), file=sys.stdout)

    def critical(self, msg, *args, **kwargs):
        self._log('critical', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log('error', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log('warning', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log('info', msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log('debug', msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._log('error', msg, *args, **kwargs)

    def close_on_exec(self):
        pass

# Usar o logger do Railway
logger_class = RailwayLogger

# Callbacks
def on_starting(server):
    server.log.info('Iniciando servidor Gunicorn no Railway...')

def post_fork(server, worker):
    server.log.info(f'Worker {worker.pid} iniciado')

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info('Reiniciando workers...')

def when_ready(server):
    server.log.info('Servidor pronto para receber conexões')

def worker_int(worker):
    worker.log.info('Worker recebeu SIGINT ou SIGQUIT')

def worker_abort(worker):
    worker.log.info('Worker recebeu SIGABRT') 