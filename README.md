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
>>> lf.get(timeout=1)
['random-img']
```

----

## management & monitoring

### flower

Access `flower` in a browser, at the host & port running it.

`flower` can be initialised in itself,
```bash
$ flower -A nibbler.app --port=5555
```
or through `celery` in order to specify additional inline configurations:

```bash
$ celery flower -A nibbler.app --address=127.0.0.1 --port=5555
```

```bash
$ celery flower -A nibbler.app --broker=amqp://guest:guest@localhost:5672//
```

### rabbitMQ

Access `rabbitmq`'s management interface in a browser, at the host & port (15672 by default) running it.

First, confirm the management interface is enabled, and (if not) run the server again to load it as a plugin:

```bash
$ rabbitmq-plugins enable rabbitmq_management
```

```bash
$ rabbitmq-server -detached
```
