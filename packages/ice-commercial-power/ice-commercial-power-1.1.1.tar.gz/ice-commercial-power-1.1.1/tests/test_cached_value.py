"""
Tests for the CachedValue class.
"""

from datetime import timedelta
import time
from icecommercialpower.utils import CachedValue


def test_has_no_value_at_start():
    """
    Test that the value is None at the start.
    """

    sut = CachedValue(timedelta(seconds=1))
    assert sut.get_value() is None


def test_has_value_after_set():
    """
    Test that the value is set after setting it.
    """
    sut = CachedValue(timedelta(seconds=10))
    sut.set_value("value")
    assert sut.get_value() == "value"


def test_has_no_value_after_reset():
    """
    Test that the value is None after resetting it.
    """
    sut = CachedValue(timedelta(seconds=10))
    sut.set_value("value")
    sut.reset()
    assert sut.get_value() is None


def test_expired_value():
    """
    Test that the value is None after expiration
    """
    sut = CachedValue(timedelta(milliseconds=10))
    sut.set_value("value")
    time.sleep(0.1)
    assert sut.get_value() is None
