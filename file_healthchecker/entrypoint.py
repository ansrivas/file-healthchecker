# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare health check for non web-apps."""

import os
import sys
from pathlib import Path
import contextlib
import functools


def __check_env_defined():
    # We expect this environment variable to be present to ensure health checks
    # A file can be like this:  /tmp/myapp.is.healthy
    __HEALTH_CHECK_FILE = os.environ.get("ENV_HEALTH_CHECK_FILE", None)
    if not __HEALTH_CHECK_FILE:
        raise Exception("Please define environment variable ENV_HEALTH_CHECK_FILE, "
                        "for e.g. `export ENV_HEALTH_CHECK_FILE=/tmp/myapp.is.healthy`")
    return __HEALTH_CHECK_FILE


def health_check():
    """Create a health check for static applications.

    Check if the healthcheck file is present else raise an exception.
    The process is like this:
    - Application initially removes this file
    - After the applications normal flow is successful, it create this file.
    - Nomad/Kubernetes invoke this application every 30s to check if the app is healthy or not.
    - This is registered as a command line application in setup.py
    """
    fname = __check_env_defined()
    filepath = Path(fname)
    if not filepath.exists():
        sys.stderr.write(f"Application is unhealthy. Health Check File not found: {fname}\n")
        raise FileNotFoundError()
    sys.stdout.write("Application is healthy")


def decorator_success(func):
    """Decorate a function to create a tmp file on each successful run.

    This function works as a wrapper, where it creates a file in case the decorated
    function is successful. Then the health_check() will check if this application was
    created or not. In case application wasn't successful, no file would be created
    and hence health_check() call will fail.

    Function's being successful means that it doesn't raise an exception in its invocation.
    for e.g.

    First decorate your function
    >>> @decorator_success
        def my_required_function():
            return True
    Now run the actual application's long running logic.

    >>> while True:
            try:
                my_required_function()
            except Exception:
                pass
            time.sleep(10)

    """
    fname = __check_env_defined()
    @functools.wraps(func)
    def wrapper_file_creator(*args, **kwargs):
        # if the file was present earlier, simply remove it
        with contextlib.suppress(FileNotFoundError):
            os.remove(fname)
        # Now execute our function
        value = func(*args, **kwargs)
        # Now create the file, if this was an exception, fill will not be created
        with open(fname, "w") as f:
            f.write("healthy")
        return value
    return wrapper_file_creator
