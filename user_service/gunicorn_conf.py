import os
import multiprocessing
from typing import Any
from gunicorn.arbiter import Arbiter
from gunicorn.workers.base import Worker
from gunicorn.http.message import Request
from gunicorn.http.wsgi import Response

# ================================
# NETWORK SETTINGS
# ================================

# Address and port Gunicorn will listen on
# Format: "HOST:PORT" or "unix:/path/to/socket.sock"
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

# Note: 0.0.0.0 means the server will be accessible on all network interfaces
# In production, Gunicorn is usually behind a reverse proxy (nginx/traefik)

# ================================
# WORKER SETTINGS
# ================================

# Number of worker processes
# Formula: (2 * CPU_COUNT) + 1 - classic recommendation for I/O bound applications
# For CPU bound tasks use CPU_COUNT
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))

# Worker process class
# uvicorn.workers.UvicornWorker - special worker for ASGI applications
# Required for FastAPI/Starlette and other async frameworks
worker_class = "uvicorn.workers.UvicornWorker"

# Alternatives for worker_class:
# - "uvicorn.workers.UvicornH11Worker" - uses h11 (pure Python HTTP)
# - "sync" - for synchronous WSGI applications (NOT for FastAPI!)
# - "gevent" - for gevent-based applications
# - "eventlet" - for eventlet-based applications

# Number of threads per worker (for sync worker_class)
threads = int(os.getenv("THREADS", 1))

# ================================
# TIMEOUT SETTINGS
# ================================

# Worker timeout (seconds)
# If worker doesn't respond longer than this, Gunicorn will kill it and start a new one
# Important: should be longer than maximum execution time of any request
timeout = int(os.getenv("TIMEOUT", 30))

# Note: for long operations (file uploads, ML inference) increase timeout
# Or move long tasks to background (Celery, RQ, etc.)

# Keep-alive timeout (seconds)
# Time to wait for next request from client on keep-alive connection
keepalive = int(os.getenv("KEEPALIVE", 2))

# Graceful timeout (seconds)
# Time given to worker to finish current requests during graceful restart/shutdown
# After this timeout expires, worker will be forcibly killed
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", 60))

# ============================================================
# WORKER LIFECYCLE
# ============================================================

# Maximum number of requests a worker will handle before restarting
# Helps combat memory leaks
# 0 = infinite (not recommended for production)
max_requests = int(os.getenv("MAX_REQUESTS", 1000))

# Random jitter for max_requests
# Prevents all workers from restarting simultaneously
# Actual max_requests will be in range [max_requests - jitter, max_requests + jitter]
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))

# Example: if max_requests=1000, jitter=50
# Worker 1 might restart after 970 requests
# Worker 2 might restart after 1030 requests
# This smooths load during restarts

# ============================================================
# LOGGING
# ============================================================

# Access log
# "-" means output to stdout (convenient for Docker/Kubernetes)
# Can specify file path: "/var/log/gunicorn/access.log"
accesslog = os.getenv("ACCESS_LOG", "-")

# Error log
# "-" means output to stderr
errorlog = os.getenv("ERROR_LOG", "-")

# Log level
# Options: "debug", "info", "warning", "error", "critical"
loglevel = os.getenv("LOG_LEVEL", "info")

# Access log format
# %(h)s - remote address
# %(l)s - "-"
# %(u)s - user name
# %(t)s - date of the request
# %(r)s - status line (e.g. GET / HTTP/1.1)
# %(s)s - status code
# %(b)s - response length
# %(f)s - referer
# %(a)s - user agent
# %(T)s - request time in seconds
# %(D)s - request time in microseconds
# %(p)s - process ID

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(T)s'

# ============================================================
# SECURITY AND PERFORMANCE
# ============================================================

# Request header size limit (bytes)
# Protection against DoS attacks with huge headers
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Maximum number of simultaneous clients in backlog
backlog = int(os.getenv("BACKLOG", 2048))

# PROCESS NAMING
# Process name (for convenience in ps/top)
proc_name = os.getenv("PROC_NAME", "gunicorn_fastapi")

# PID file (optional)
# pidfile = '/var/run/gunicorn.pid'

# Working directory
chdir = os.getenv("CHDIR", ".")

# User/group for daemonization (requires root)
# user = 'www-data'
# group = 'www-data'

# ================================
# SERVER HOOKS (optional)
# ================================


def on_starting(server: Arbiter):
    """
    Called before master process starts
    Useful for initializing shared resources
    """
    server.log.info("Gunicorn master starting")


def on_reload(server: Arbiter):
    """
    Called when reloading configuration
    """
    server.log.info("Gunicorn reloading")


def when_ready(server: Arbiter):
    """
    Called when server is ready to accept requests
    Useful for health checks
    """
    server.log.info("Gunicorn is ready. Spawning workers")


def pre_fork(server: Arbiter, worker: Worker):
    """
    Called before forking worker process
    """
    pass


def post_fork(server: Arbiter, worker: Worker):
    """
    Called after forking worker process
    Useful for initializing per-worker resources (DB connections, etc.)
    """
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def pre_exec(server: Arbiter):
    """
    Called before new exec during reload
    """
    server.log.info("Forked child, re-executing.")


def worker_int(worker: Worker):
    """
    Called when worker receives SIGINT or SIGQUIT
    """
    worker.log.info(f"Worker received INT or QUIT signal (pid: {worker.pid})")


def worker_abort(worker: Worker):
    """
    Called when worker receives SIGABRT (usually on timeout)
    """
    worker.log.warning(f"Worker received SIGABRT signal (pid: {worker.pid})")


def pre_request(worker: Worker, req: Request):
    """
    Called before processing each request
    """
    worker.log.debug(f"Request start: {req.method} {req.path}")


def post_request(worker: Worker, req: Request, environ: dict[str, Any], resp: Response):
    """
    Called after processing each request
    """
    worker.log.debug(f"Request finish: {req.method} {req.path}")


def worker_exit(server: Arbiter, worker: Worker):
    """
    Called when worker exits
    """
    server.log.info(f"Worker exiting (pid: {worker.pid})")


def on_exit(server: Arbiter):
    """
    Called when master process exits
    """
    server.log.info("Gunicorn master shutting down")
