""" Tests for get_tracer """
# pylint: disable=too-few-public-methods,missing-class-docstring
from opencensus.trace.tracers.noop_tracer import NoopTracer
from icecommercialpower.observability import get_tracer


def test_get_tracer_from_empty_context_returns_no_op_tracer():
    """
    Tests that get_tracer returns no-op tracer when context is empty
    """

    # Arrange
    class MyContext:
        def __init__(self, other_prop):
            self.other_prop = other_prop

    context = MyContext("test")

    # Act
    actual = get_tracer(context)

    # Assert
    assert isinstance(actual, NoopTracer)


def test_get_tracer_from_invalid_context_returns_no_op_tracer():
    """
    Tests that get_tracer returns no-op tracer when context is invalid
    """

    # Act
    context = None
    actual = get_tracer(context)

    # Assert
    assert isinstance(actual, NoopTracer)


def test_get_tracer_from_non_empty_context_returns_tracer():
    """
    Tests that get_tracer returns tracer when context is valid
    """

    # Arrange
    class MyContext:
        def __init__(self, tracer):
            self.tracer = tracer

    tracer = object()
    context = MyContext(tracer)

    # Act
    actual = get_tracer(context)

    # Assert
    assert actual == tracer
