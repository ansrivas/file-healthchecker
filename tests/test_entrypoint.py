# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the entry point."""

import pytest
import os
import tempfile


def test_health_check_missing_env():
    from file_healthchecker.entrypoint import health_check
    # Without environment definition this should raise an exception
    with pytest.raises(Exception):
        health_check()


def test_health_check_set_env():
    tfile = tempfile.NamedTemporaryFile()
    os.environ["ENV_HEALTH_CHECK_FILE"] = tfile.name

    from file_healthchecker.entrypoint import health_check
    # At this point no exception should be raised
    health_check()
