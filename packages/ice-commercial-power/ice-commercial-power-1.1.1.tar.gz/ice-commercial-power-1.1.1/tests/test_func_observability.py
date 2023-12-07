""" Tests for FuncObservability """
# pylint: disable=too-few-public-methods,missing-class-docstring
from unittest import mock
from icecommercialpower.observability import FuncObservability

APP_INSIGHTS_ENV_KEY = "APPINSIGHTS_INSTRUMENTATIONKEY"


def setup_function():
    """
    Setup function
    """
    # pylint: disable=protected-access
    FuncObservability._configured = False


def test_initialize_only_runs_once(monkeypatch):

    """
    Tests that initialize only runs once
    """

    # Arrange
    monkeypatch.setenv(APP_INSIGHTS_ENV_KEY, "AAABBBCCC")

    # Act
    with mock.patch(
        "opencensus.trace.config_integration.trace_integrations"
    ) as trace_integrations, mock.patch(
        "opencensus.extension.azure.functions.OpenCensusExtension.configure"
    ) as configure:
        FuncObservability.initialize()
        FuncObservability.initialize()
        trace_integrations.assert_called_once()
        configure.assert_called_once()


def test_initialize_checks_instrumentation_key(monkeypatch):

    """
    Tests that initialize checks for instrumentation key
    """

    # Arrange
    monkeypatch.setenv(APP_INSIGHTS_ENV_KEY, "")

    with mock.patch(
        "opencensus.trace.config_integration.trace_integrations"
    ) as trace_integrations, mock.patch(
        "opencensus.extension.azure.functions.OpenCensusExtension.configure"
    ) as configure:
        FuncObservability.initialize()
        FuncObservability.initialize()
        trace_integrations.assert_not_called()
        configure.assert_not_called()
