import os
import sys

# Configurações básicas
bind = "0.0.0.0:8080"
workers = 2
threads = 4
worker_class = "gthread"
timeout = 120

# Configuração de logs
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Formato de log personalizado para o Railway
def on_starting(server):
    """Callback executado quando o servidor inicia"""
    server.log.info("Server is starting up")

def post_fork(server, worker):
    """Callback executado após o fork de cada worker"""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_fork(server, worker):
    """Callback executado antes do fork de cada worker"""
    pass

def pre_exec(server):
    """Callback executado antes do exec de cada worker"""
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    """Callback executado quando o servidor está pronto"""
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    """Callback executado quando um worker recebe SIGINT ou SIGQUIT"""
    worker.log.info("worker received INT or QUIT signal")

def worker_abort(worker):
    """Callback executado quando um worker recebe SIGABRT"""
    worker.log.info("worker received SIGABRT signal")

# Configuração de log personalizada
class CustomLogger:
    def __init__(self, app):
        self.app = app
        self.error_log = sys.stderr
        self.access_log = sys.stdout
        self.loglevel = "info"
        self.access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

    def critical(self, msg, *args, **kwargs):
        self.error_log.write(f"[CRITICAL] {msg}\n")

    def error(self, msg, *args, **kwargs):
        self.error_log.write(f"[ERROR] {msg}\n")

    def warning(self, msg, *args, **kwargs):
        self.error_log.write(f"[WARNING] {msg}\n")

    def info(self, msg, *args, **kwargs):
        self.error_log.write(f"[INFO] {msg}\n")

    def debug(self, msg, *args, **kwargs):
        self.error_log.write(f"[DEBUG] {msg}\n")

    def exception(self, msg, *args, **kwargs):
        self.error_log.write(f"[EXCEPTION] {msg}\n")

# Configuração do logger
logger_class = CustomLogger 