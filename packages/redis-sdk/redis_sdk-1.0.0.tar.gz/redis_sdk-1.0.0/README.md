# Khulnasoft Redis Python SDK

redis-sdk is a connectionless, HTTP-based Redis client for Python, designed to be used in serverless and serverful environments such as:
- AWS Lambda
- Vercel Serverless
- Google Cloud Functions
- and other environments where HTTP is preferred over TCP.

Inspired by other Redis clients like [@khulnasoft/redis](https://github.com/khulnasoft-lab/redis-sdk) and [redis-py](https://github.com/redis/redis-py),
the goal of this SDK is to provide a simple way to use Redis over the [Khulnasoft REST API](https://docs.khulnasoft.com/redis/features/restapi).

The SDK is currently compatible with Python 3.8 and above.

<!-- toc -->

- [Khulnasoft Redis Python SDK](#redis-sdk-python-sdk)
- [Quick Start](#quick-start)
  - [Install](#install)
    - [PyPI](#pypi)
  - [Usage](#usage)
    - [BITFIELD and BITFIELD\_RO](#bitfield-and-bitfield_ro)
    - [Custom commands](#custom-commands)
- [Encoding](#encoding)
- [Retry mechanism](#retry-mechanism)
- [Contributing](#contributing)
  - [Preparing the environment](#preparing-the-environment)
  - [Running tests](#running-tests)

<!-- tocstop -->

# Quick Start

## Install

### PyPI
```bash
pip install redis-sdk
```

## Usage
To be able to use redis-sdk, you need to create a database on [Khulnasoft](https://console.khulnasoft.com/)
and grab `REDIS_SDK_REST_URL` and `REDIS_SDK_REST_TOKEN` from the console.

```python
# for sync client
from redis_sdk import Redis

redis = Redis(url="REDIS_SDK_REST_URL", token="REDIS_SDK_REST_TOKEN")

# for async client
from redis_sdk.asyncio import Redis

redis = Redis(url="REDIS_SDK_REST_URL", token="REDIS_SDK_REST_TOKEN")
```

Or, if you want to automatically load the credentials from the environment:

```python
# for sync use
from redis_sdk import Redis
redis = Redis.from_env()

# for async use
from redis_sdk.asyncio import Redis
redis = Redis.from_env()
```

If you are in a serverless environment that allows it, it's recommended to initialise the client outside the request handler
to be reused while your function is still hot.

Running commands might look like this:

```python
from redis_sdk import Redis

redis = Redis.from_env()

def main():
  redis.set("a", "b")
  print(redis.get("a"))

# or for async context:

from redis_sdk.asyncio import Redis

redis = Redis.from_env()

async def main():  
  await redis.set("a", "b")
  print(await redis.get("a"))
```

### BITFIELD and BITFIELD_RO
One particular case is represented by these two chained commands, which are available as functions that return an instance of 
the `BITFIELD` and, respectively, `BITFIELD_RO` classes. Use the `execute` function to run the commands.

```python
redis.bitfield("test_key") \
  .incrby(encoding="i8", offset=100, increment=100) \
  .overflow("SAT") \
  .incrby(encoding="i8", offset=100, increment=100) \
  .execute()

redis.bitfield_ro("test_key_2") \
  .get(encoding="u8", offset=0) \
  .get(encoding="u8", offset="#1") \
  .execute()
```

### Custom commands
If you want to run a command that hasn't been implemented, you can use the `execute` function of your client instance
and pass the command as a `list`.

```python
redis.execute(command=["XLEN", "test_stream"])
```

# Encoding
Although Redis can store invalid JSON data, there might be problems with the deserialization.
To avoid this, the Khulnasoft REST proxy is capable of encoding the data as base64 on the server and then sending it to the client to be
decoded. 

For very large data, this can add a few milliseconds in latency. So, if you're sure that your data is valid JSON, you can set
`rest_encoding` to `None`.

# Retry mechanism
redis-sdk has a fallback mechanism in case of network or API issues. By default, if a request fails it'll retry once, 3 seconds 
after the error. If you want to customize that, set `rest_retries` and `rest_retry_interval` (in seconds).

# Contributing

## Preparing the environment
This project uses [Poetry](https://python-poetry.org) for packaging and dependency management. Make sure you are able to create the poetry shell with relevant dependencies.

You will also need a database on [Khulnasoft](https://console.khulnasoft.com/).

## Running tests
To run all the tests, make sure the poetry virtual environment activated with all 
the necessary dependencies. Set the `REDIS_SDK_REST_URL` and `REDIS_SDK_REST_TOKEN` environment variables and run:

```bash
poetry run pytest
```