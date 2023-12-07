"""Test for dummy sms client"""

import logging
from uuid import UUID
from unittest import mock
from icecommercialpower.sms import DummySmsClient


@mock.patch("uuid.uuid4")
def test_dummy_sms_client_send_sms(uuid_mock: mock.MagicMock, caplog):
    """Test the dummy sms client that just logs the call to send_sms"""

    # arrange
    with caplog.at_level(logging.INFO):
        test_sid = UUID("70fc8f47-201b-474c-985f-a7902354fc5f")
        uuid_mock.return_value = test_sid

        client = DummySmsClient()
        phone = "+123456789"
        msg = "My test message"

        # act
        client.send_sms(phone, msg)

        # assert
        expected_msg = f"Test SMS Client: send_sms: to: ****{phone[-3:]}, body: {msg}, sid: {str(test_sid)}"  # pylint: disable=line-too-long
        assert expected_msg in caplog.text
