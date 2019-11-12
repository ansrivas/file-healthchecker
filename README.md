# file-healthchecker

Use this application to monitor your long running "non-web" application's health check.

[![Build Status](https://travis-ci.com/ansrivas/healthcheck.svg?token=hM6V8mr5fwQPseiFSYVi&branch=master)](https://travis-ci.com/ansrivas/healthcheck)

## Installation

### pip

```
pip install file-healthchecker
```

## Use Case

Lets say we have a service which needs to perform some action every x-duration.
In python-world we would simply run it inside a while loop and invoke it every x-minutes.

Now define an environment var `ENV_HEALTH_CHECK_FILE` which will represent a file creation
in case the app is healthy. for e.g. `export ENV_HEALTH_CHECK_FILE=/tmp/myapp.is.healthy`

This following snippet will perform following tasks:

- Every invocation of my_application will first remove a health-check file.
- Run the application
- NOTE: Raise an exception in case the application is failing. Handle it outside, as show in the given example.
- If no exception is raised, the decorator will create a file defined by the env-var `ENV_HEALTH_CHECK_FILE`

```python
from file_healthchecker import decorator_success
import time

@decorator_success
def my_application():
    ... doing lots of work
    ... more work
    # in case of failure, raise exception
    return True

if __name__ == "__main__":
    while True:
        try:
            my_application()
        except Exception:
            pass
        time.sleep(10)

```
With the installation another cmd-app also gets installed - `checkhealth`.

How to check application's health?
- One can simply run `ENV_HEALTH_CHECK_FILE=/tmp/myapp.is.healthy checkhealth` at regular intervals or
- pass this command to orchestrators like `Nomad`, `Kubernetes`, etc. as a part of their health-check commands.

## Current Stable Version

```
0.1.0
```

### Development Installation

- Clone the project.
- Now install the application in editable mode and you are ready to start development

```
$ pip install -e .
```

## Test

To run the tests:

```
make test
```

## License

MIT
