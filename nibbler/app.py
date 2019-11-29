import requests
from pathlib import Path
from celery import Celery


DATA_DIR = 'nibbler/downloaded/'

downloader = Celery(
        'downloader',
        backend = 'rpc://',  # RPC result backend for AMQP broker
        broker  = 'pyamqp://guest@localhost//'  # RabbitMQ broker location
)


@downloader.task
def download(url: str, f_name: str):

    resp = requests.get(url)
    resp.raise_for_status()

    data  = resp.content
    f_loc = Path.cwd() / DATA_DIR / f_name

    with open(f_loc, 'wb') as f:
        f.write(data)


@downloader.task
def list_files():

    files = Path(DATA_DIR).iterdir()

    return [f.name for f in files if f.is_file()]
