"""
Test for TwilioSmsClient
"""
# pylint: disable=duplicate-code
import logging
from unittest import mock
import pytest
from pytest import mark
from twilio.base.exceptions import TwilioRestException
from icecommercialpower.sms import TwilioSmsClient


@mark.parametrize(
    "fixed_sms_number, to_number, expected_number",
    [
        ("19998877", "11234567", "19998877"),
        (None, "11234567", "11234567"),
        ("", "11234567", "11234567"),
    ],
)
def test_send_sms_succeeds(
    fixed_sms_number: str,
    to_number: str,
    expected_number: str,
    caplog: pytest.LogCaptureFixture,
):
    """Test that send_sms() returns True when the message is sent successfully"""
    # Arrange
    with caplog.at_level(logging.INFO):
        message = "Test message"
        expected_sid = "Test Sid"
        from_number = "+15556677"
        mock_client = mock.MagicMock()
        mock_client.messages.create.return_value.sid = expected_sid

        sut = TwilioSmsClient(
            client=mock_client,
            from_number=from_number,
            fixed_sms_number=fixed_sms_number,
        )

        # Act
        sid = sut.send_sms(to_number, message)

        # Assert
        assert mock_client.messages.create.called is True
        assert sid == expected_sid

        expected_msg = (
            f"Sending message {message} to {expected_number} through Twilio..."
        )
        assert expected_msg in caplog.text


def test_send_sms_throws():
    """Test that send_sms() throws an exception when the message is not sent successfully"""

    # Arrange
    message = "Hi there"
    from_number = "71238"
    to_number = "<your-personal-number>"
    mock_client = mock.MagicMock()
    mock_client.messages.create.side_effect = TwilioRestException(
        status="Status", uri="Uri", msg="Test"
    )

    sut = TwilioSmsClient(client=mock_client, from_number=from_number)

    # Act and Assert
    with pytest.raises(TwilioRestException) as ex:
        sut.send_sms(to_number, message)
        assert ex.msg == "Test"

    assert mock_client.messages.create.called is True
