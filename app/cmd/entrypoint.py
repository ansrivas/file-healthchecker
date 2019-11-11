# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare health check for non web-apps."""

import os
import sys
from pathlib import Path
import contextlib
import functools

# We expect this environment variable to be present to ensure health checks
# A file can be like this:  /tmp/myapp.is.healthy
__HEALTH_CHECK_FILE = os.environ.get("ENV_HEALTH_CHECK_FILE", None)
if not __HEALTH_CHECK_FILE:
    raise Exception("Please define environment variable ENV_HEALTH_CHECK_FILE, "
            "for e.g. `export ENV_HEALTH_CHECK_FILE=/tmp/myapp.is.healthy`")

def health_check():
    """Create a health check for static applications.

    Check if the healthcheck file is present else raise an exception.
    The process is like this:
    - Application initially removes this file
    - After the applications normal flow is successful, it create this file.
    - Nomad/Kubernetes invoke this application every 30s to check if the app is healthy or not.
    - This is registered as a command line application in setup.py
    """
    filepath = Path(__HEALTH_CHECK_FILE)
    if not filepath.exists():
        sys.stderr.write(f"Application is unhealthy. Health Check File not found: {__HEALTH_CHECK_FILE}\n")
        raise FileNotFoundError()
    sys.stdout.write("Application is healthy")


def decorator_success(func):
    """Decorate a function to create a tmp file on each successful run."""
    @functools.wraps(func)
    def wrapper_file_creator(*args, **kwargs):
        # if the file was present earlier, simply remove it
        with contextlib.suppress(FileNotFoundError):
            os.remove(__HEALTH_CHECK_FILE)
        # Now execute our function
        value = func(*args, **kwargs)
        # Now create the file, if this was an exception, fill will not be created
        with open(__HEALTH_CHECK_FILE, "w") as f:
            f.write("healthy")
        return value
    return wrapper_file_creator
