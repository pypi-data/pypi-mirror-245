"""
Tests for the mailgun handler
"""

import logging
import os
import json
from unittest import mock
from urllib.parse import urlencode
from urllib.parse import unquote
import httpretty
import pytest
import requests
from icecommercialpower.mailgun import MailgunHandler


@pytest.fixture(autouse=True)
def set_mailgun_env(monkeypatch):
    """
    sets ENV values for tests with mailgun handler
    """
    # creates some test settings for the mailgun handler
    monkeypatch.setenv("MAILGUN_API_ENDPOINT", "http://testmailgun/message")
    monkeypatch.setenv("MAILGUN_API_KEY", "12345")
    monkeypatch.setenv("MAILGUN_FROM_ADDRESS", "foo@b.ar")
    monkeypatch.setenv("MAILGUN_TO_ADDRESSES", "test@icecommpower.com")
    monkeypatch.setenv("MAILGUN_MAX_RETRIES", "3")


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("status_code", [200, 201, 202])
def test_mailgun_request(status_code: int):
    """
    Simple request processing test to ensure payload POSTed to url matches expectations
    """
    # registers a handler for httpretty,
    # so it intercepts the http call (vs passing it to the network stack)
    httpretty.register_uri(
        httpretty.POST,
        os.environ["MAILGUN_API_ENDPOINT"],
        f'{{"from": {os.environ["MAILGUN_FROM_ADDRESS"]}, \
        "to": [{os.environ["MAILGUN_TO_ADDRESSES"]}], \
        "subject": "test alert","text": "this is only a test"}}',
        status=status_code,
    )

    handler = MailgunHandler()
    result = handler.send_alert_mail("test alert", "this is only a test")

    # assert the request body is as expected
    req = httpretty.last_request()
    body = unquote(req.body.decode("UTF-8"))
    expected = "from=foo@b.ar&to=test@icecommpower.com&subject=test+alert&text=this+is+only+a+test"

    assert body == expected
    assert result is True


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_mailgun_retry_request():
    """
    Request test, which ensures that the retry configuration
    handles some temporary failures before succeeding
    """
    retry_count = 0

    def mock_request_handler(request, uri, response_headers):
        expected_body = urlencode(
            {
                "from": "foo@b.ar",
                "to": "test@icecommpower.com",
                "subject": "test alert",
                "text": "this is only a test",
            }
        )
        assert uri == os.environ["MAILGUN_API_ENDPOINT"]
        assert request.body == expected_body.encode("UTF-8")
        nonlocal retry_count

        # cause an error status to be returned for a few requests, to make sure that
        # the client has to retry
        if retry_count < 2:
            retry_count += 1
            return [500, response_headers, json.dumps({"error": "unknown"})]
        return [
            200,
            response_headers,
            json.dumps({"error": "none"}),
        ]

    httpretty.register_uri(
        httpretty.POST, os.environ["MAILGUN_API_ENDPOINT"], body=mock_request_handler
    )
    handler = MailgunHandler()
    result = handler.send_alert_mail("test alert", "this is only a test")

    assert retry_count == 2
    assert result is True


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_mailgun_failing():
    """
    Request test, which ensures that false is returned if Mailgun returns status != 200
    """

    def mock_request_handler(request, uri, response_headers):
        expected_body = urlencode(
            {
                "from": "foo@b.ar",
                "to": "test@icecommpower.com",
                "subject": "test alert",
                "text": "this is only a test",
            }
        )
        assert uri == os.environ["MAILGUN_API_ENDPOINT"]
        assert request.body == expected_body.encode("UTF-8")
        return [400, response_headers, json.dumps({"error": "unknown"})]

    httpretty.register_uri(
        httpretty.POST, os.environ["MAILGUN_API_ENDPOINT"], body=mock_request_handler
    )
    handler = MailgunHandler()
    result = handler.send_alert_mail("test alert", "this is only a test")

    assert result is False


@mock.patch("requests.Session.post")
def test_mailgun_timeout(post_mock, caplog):
    """
    Request test, which ensures that the timeout configuration
    works
    """
    post_mock.side_effect = requests.Timeout

    handler = MailgunHandler()
    with caplog.at_level(logging.ERROR):

        result = handler.send_alert_mail("test alert", "this is only a test")

        assert result is False
        assert (
            "Error trying to send low balance notification mail via Mailgun"
            in caplog.text
        )
        assert "Timeout" in caplog.text
