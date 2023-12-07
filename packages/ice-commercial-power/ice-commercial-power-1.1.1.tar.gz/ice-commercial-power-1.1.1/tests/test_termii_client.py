"""
Tests for the termii handler
"""
# pylint: disable=duplicate-code
import json
import logging
import os
from unittest import mock
import httpretty
import pytest
from pytest import mark
import requests
from icecommercialpower.sms import TermiiClient


@pytest.fixture(autouse=True)
def set_termii_env(monkeypatch):
    """
    Sets ENV values for tests with termii handler
    """
    # creates some test settings for the termii handler
    monkeypatch.setenv("TERMII_API_ENDPOINT", "http://testtermii/message")
    monkeypatch.setenv("TERMII_API_KEY", "12345")
    monkeypatch.setenv("TERMII_FROM_ADDRESS", "Test")
    monkeypatch.setenv("TERMII_CHANNEL", "generic")
    monkeypatch.setenv("TERMII_MAX_RETRIES", "10")


@mark.parametrize(
    "fixed_sms_number, to_sms_number, expected_number",
    [
        ("17778899", "13212211", "17778899"),
        (None, "13212211", "13212211"),
        ("", "13212211", "13212211"),
    ],
)
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_termii_request(
    fixed_sms_number: str,
    to_sms_number: str,
    expected_number: str,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    Simple request processing test to ensure payload POSTed to url matches expectations
    """
    # registers a handler for httpretty,
    # so it intercepts the http call (vs passing it to the network stack)

    httpretty.register_uri(
        method=httpretty.POST,
        uri=os.environ["TERMII_API_ENDPOINT"],
        body='{"message_id": "9122821270554876574", "message": "Successfully Sent", '
        '"balance": 9, "user": "Test User"}',
    )

    if fixed_sms_number is not None:
        monkeypatch.setenv("FIXED_SMS_NUMBER", fixed_sms_number)

    sut = TermiiClient.from_env()
    result = sut.send_sms(to_sms_number, "Test SMS")

    # assert the request body is as expected
    body = json.loads(httpretty.last_request().body.decode("UTF-8"))
    expected_sent_req = {
        "api_key": "12345",
        "channel": "generic",
        "from": "Test",
        "sms": "Test SMS",
        "to": expected_number,
        "type": "plain",
    }

    assert body == expected_sent_req
    assert result == "9122821270554876574"


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_termii_retry_request():
    """
    Request test, which ensures that the retry configuration
    handles some temporary failures before succeeding
    """
    retry_count = 0
    expected_message_id = "9122821270554876574"
    max_retries = 3

    def mock_request_handler(request, uri, response_headers):
        expected_body = {
            "to": "11234567",
            "from": "Test",
            "sms": "Test SMS",
            "type": "plain",
            "channel": "generic",
            "api_key": "12345",
        }
        assert uri == os.environ["TERMII_API_ENDPOINT"]
        assert json.loads(request.body) == expected_body
        nonlocal retry_count

        # cause an error status to be returned for a few requests, to make sure that
        # the client has to retry

        if retry_count < max_retries:
            retry_count = retry_count + 1
            return [500, response_headers, json.dumps({"error": "unknown"})]
        return [
            200,
            response_headers,
            json.dumps(
                {
                    "message_id": expected_message_id,
                    "message": "Successfully Sent",
                    "balance": 9,
                    "user": "Test User",
                }
            ),
        ]

    httpretty.register_uri(
        method=httpretty.POST,
        uri=os.environ["TERMII_API_ENDPOINT"],
        body=mock_request_handler,
    )
    sut = TermiiClient.from_env()
    result = sut.send_sms("11234567", "Test SMS")

    assert result == expected_message_id
    assert retry_count == max_retries


@mock.patch("requests.Session.post")
def test_termii_timeout(post_mock, caplog):
    """
    Request test, which ensures that the timeout configuration
    works
    """
    post_mock.side_effect = requests.Timeout

    sut = TermiiClient.from_env()
    with caplog.at_level(logging.ERROR):

        result = sut.send_sms("11234567", "Test SMS")

        assert result is None
        assert "Error sending SMS via Termii." in caplog.text
        assert "Timeout" in caplog.text
