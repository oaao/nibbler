# nibbler
celery + rabbitMQ task handling

## setup

1. Install RabbitMQ

    > This will also start RabbitMQ with default configuration.

    ```bash
    $ apt-get install rabbitmq-server
    ```

2. Install Python dependencies (or use the provided `Pipfile` and `Pipfile.lock`):

```bash
# using pipenv
$ pipenv install --dev

# or
$ pip install celery flower
```


## usage

1. Start the `celery` worker:

```bash
$ celery -A nibbler.app worker
```

2. In another terminal, enter a Python shell in your virtual environment.

3. Submit a job to RabbitMQ and observe its completion:

> Let's get a random image from httpbin:

```python
>>> from nibbler import app
>>> resp = app.download.delay(  # delay submits to RabbitMQ (async)
...     'https://httpbin.org/image/jpeg',
...     'random-img'
... )
```

> And then inspect the task. See also `resp.traceback`, or the Celery terminal itself.

```python
>>> resp.ready()  # check whether task has finished
True
>>> resp.status
'SUCCESS'
>>> app.list_files()  # watch out - this is a synchronous call, just for brevity
['random-img']
```

> Let's perform the `list_files` task properly now - i.e., also asynchronously:

```python
>>> lf = app.list_files.delay()
>>> lf.ready()
True
>>> # without a timeout kwarg, the client waits for the task to finish synchronously
>>> l.get(timeout=1)
['random-img']
```
