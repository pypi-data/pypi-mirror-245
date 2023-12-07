# pylint: disable=missing-function-docstring,missing-module-docstring
import json
import logging
import os
from typing import Optional
from unittest import mock
from datetime import datetime, timezone
import uuid
import requests
from requests import HTTPError
from requests.exceptions import RetryError, Timeout

import httpretty
import pytest
from icecommercialpower.flutterwave import (
    FlutterWaveClient,
    FwPaymentType,
    FwTransaction,
    FwTransactionStatus,
    FwStartUssdPaymentRequest,
    FlutterWaveResponseError,
)

# pylint: disable=too-many-arguments
def create_charges_response(
    tx_ref: str,
    amount: float,
    customer_name: str,
    customer_phone: str,
    customer_email: str,
    payment_code: str,
    fw_transaction_id: str,
    flw_ref: str,
    payment_ussd_code: str,
    currency: str,
    app_fee: float = 0,
):
    """Creates a response for charges"""
    return f"""
{{
    "status": "success",
    "message": "Charge initiated",
    "data": {{
        "id": {fw_transaction_id},
        "tx_ref": "{tx_ref}",
        "flw_ref": "{flw_ref}",
        "device_fingerprint": "N/A",
        "amount": {amount},
        "charged_amount": {amount + app_fee},
        "app_fee": {app_fee},
        "merchant_fee": 0,
        "processor_response": "Transaction in progress",
        "auth_model": "USSD",
        "currency": "{currency}",
        "ip": "127.0.0.1",
        "narration": "test",
        "status": "pending",
        "payment_type": "ussd",
        "fraud_status": "ok",
        "charge_type": "normal",
        "created_at": "2021-12-20T10:14:09.000Z",
        "account_id": 1037512,
        "customer": {{
            "id": 999,
            "phone_number": "{customer_phone}",
            "name": "{customer_name}",
            "email": "{customer_email}",
            "created_at": "2021-12-10T10:45:26.000Z"
        }},
        "payment_code": "{payment_code}"
    }},
    "meta": {{
        "authorization": {{
            "mode": "ussd",
            "note": "{payment_ussd_code}"
        }}
    }}
}}"""


@pytest.mark.parametrize(
    ["status", "expected_status"],
    [
        ["successful", FwTransactionStatus.SUCCESSFUL],
        ["abandoned", FwTransactionStatus.ABANDONED],
        ["pending", FwTransactionStatus.PENDING],
        ["cancelled", FwTransactionStatus.CANCELLED],
        ["voided", FwTransactionStatus.VOIDED],
        ["failed", FwTransactionStatus.FAILED],
    ],
)
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_transaction_status_parses_result_correctly(status: str, expected_status):
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    tx_id = 2626270

    valid_response = {
        "status": "success",
        "message": "Transaction fetched successfully",
        "data": {
            "id": tx_id,
            "tx_ref": "a_012345678901234567890123456789012345678901234567",
            "flw_ref": "OVQD0223216369822423",
            "device_fingerprint": "N/A",
            "amount": 1500,
            "currency": "NGN",
            "charged_amount": 1500,
            "app_fee": 481.5,
            "merchant_fee": 0,
            "processor_response": "Transaction completed",
            "auth_model": "USSD",
            "ip": "52.209.154.143",
            "narration": "FLUTTERWAVE V3 DOCS",
            "status": status,
            "payment_type": "ussd",
            "created_at": "2021-11-15T13:17:21.000Z",
            "account_id": 118468,
            "meta": {
                "customer_id": "123456789",
            },
            "amount_settled": 1018.5,
            "customer": {
                "id": 799459,
                "name": "Anonymous Customer",
                "phone_number": "07033002245",
                "email": "user@flw.com",
                "created_at": "2021-03-13T11:41:54.000Z",
            },
        },
    }

    def callback(request, _, response_headers):
        assert request.headers.get("Authorization") == "Bearer " + test_secret_key
        return [200, response_headers, json.dumps(valid_response)]

    httpretty.register_uri(
        httpretty.GET,
        f"https://api.flutterwave.com/v3/transactions/{tx_id}/verify",
        body=callback,
    )

    # Act
    resp = client.get_transaction_status(tx_id)

    # Assert
    expected = FwTransaction(
        transaction_id=valid_response["data"]["id"],
        flw_ref=valid_response["data"]["flw_ref"],
        tx_ref=valid_response["data"]["tx_ref"],
        status=expected_status,
        currency=valid_response["data"]["currency"],
        amount=float(valid_response["data"]["amount"]),
        customer_phone=valid_response["data"]["customer"]["phone_number"],
        customer_email=valid_response["data"]["customer"]["email"],
        customer_name=valid_response["data"]["customer"]["name"],
        created_at=datetime(2021, 11, 15, 13, 17, 21, tzinfo=timezone.utc),
        customer_id=int(valid_response["data"]["meta"]["customer_id"]),
        payment_type=FwPaymentType.USSD.value,
        amount_settled=float(valid_response["data"]["amount_settled"]),
        app_fee=float(valid_response["data"]["app_fee"]),
        merchant_fee=float(valid_response["data"]["merchant_fee"]),
        charged_amount=float(valid_response["data"]["charged_amount"]),
    )

    assert resp == expected


@mock.patch.object(FlutterWaveClient, "__init__", return_value=None)
def test_from_env_ctor(fw_client_cls, monkeypatch):
    # Arrange
    test_secret_key = "testsecret"
    monkeypatch.setenv("FLUTTERWAVE_SECRET_KEY", test_secret_key)

    # Act
    FlutterWaveClient.from_env()

    # Assert
    assert fw_client_cls.called_once_with(mock.ANY, "Bearer " + test_secret_key)


@pytest.mark.parametrize("status_code", [401, 403, 404])
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_ussd_transation_not_retriable_bad_response_code(status_code: int):
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    httpretty.register_uri(
        httpretty.POST,
        "https://api.flutterwave.com/v3/charges?type=ussd",
        status=status_code,
    )

    # Act & Assert
    with pytest.raises(HTTPError):
        client.start_ussd_payment(create_start_ussd_request())


@pytest.mark.parametrize("status_code", [400, 500, 503])
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_ussd_transation_retriable_bad_response_code(status_code: int):
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    httpretty.register_uri(
        httpretty.POST,
        "https://api.flutterwave.com/v3/charges?type=ussd",
        status=status_code,
    )

    # Act & Assert
    with pytest.raises(RetryError):
        client.start_ussd_payment(create_start_ussd_request())


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_ussd_transation_status_not_success():
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    httpretty.register_uri(
        httpretty.POST,
        "https://api.flutterwave.com/v3/charges?type=ussd",
        body="""
        {
            "status": "error",
            "message": "Transaction Reference already exist. Try again in 2 minutes time to use the same ref for a new transaction",
            "data": null
        }""",
    )

    # Act & Assert
    with pytest.raises(FlutterWaveResponseError) as err:
        client.start_ussd_payment(create_start_ussd_request())

    assert (
        str(err.value) == "Transaction Reference already exist. "
        "Try again in 2 minutes time to use the same ref for a new transaction"
    )


def create_start_ussd_request() -> FwStartUssdPaymentRequest:
    """Creates a test request for starting a ussd payment"""
    return FwStartUssdPaymentRequest(
        tx_ref=str(uuid.uuid4()),
        account_bank="044",
        amount=1000,
        currency="NGN",
        customer_phone="0123456789",
        customer_email="test@email.com",
        customer_name="Ana Testing",
        customer_id=1000,
    )


@pytest.mark.parametrize("app_fee", [0.0, 10.0])
@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_ussd_transaction_succeeds(app_fee: Optional[float]):
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    start_request = create_start_ussd_request()
    payment_code = "12345"
    fw_transaction_id = 90000
    flw_ref = "INOT1111111111111111"
    payment_ussd_code = "*889*767*8972#"

    httpretty.register_uri(
        httpretty.POST,
        "https://api.flutterwave.com/v3/charges?type=ussd",
        body=create_charges_response(
            tx_ref=start_request.tx_ref,
            amount=start_request.amount,
            customer_phone=start_request.customer_phone,
            customer_email=start_request.customer_email,
            customer_name=start_request.customer_name,
            currency=start_request.currency,
            app_fee=app_fee,
            payment_code=payment_code,
            fw_transaction_id=fw_transaction_id,
            flw_ref=flw_ref,
            payment_ussd_code=payment_ussd_code,
        ),
    )

    # Act
    resp = client.start_ussd_payment(request=start_request)

    # Assert
    assert (
        httpretty.last_request().headers.get("Authorization")
        == "Bearer " + test_secret_key
    )
    assert json.loads(httpretty.last_request().body) == {
        "tx_ref": start_request.tx_ref,
        "account_bank": start_request.account_bank,
        "amount": start_request.amount,
        "currency": start_request.currency,
        "email": start_request.customer_email,
        "phone_number": start_request.customer_phone,
        "fullname": start_request.customer_name,
        "meta": {
            "customer_id": start_request.customer_id,
        },
    }

    assert resp.payment_code == payment_code
    assert resp.ussd_code == payment_ussd_code
    assert resp.transaction == FwTransaction(
        tx_ref=start_request.tx_ref,
        currency=start_request.currency,
        amount=start_request.amount,
        customer_id=start_request.customer_id,
        customer_email=start_request.customer_email,
        customer_name=start_request.customer_name,
        customer_phone=start_request.customer_phone,
        app_fee=app_fee,
        merchant_fee=0.0,
        charged_amount=start_request.amount + app_fee,
        amount_settled=None,
        status=FwTransactionStatus.PENDING,
        created_at=datetime(2021, 12, 20, 10, 14, 9, 0, tzinfo=timezone.utc),
        flw_ref=flw_ref,
        payment_type=FwPaymentType.USSD.value,
        transaction_id=fw_transaction_id,
    )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_ussd_transaction_retries_succeeds():
    """Tests creating a ussd transaction with retries"""
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    start_request = create_start_ussd_request()
    payment_code = "12345"
    fw_transaction_id = 90000
    flw_ref = "INOT1111111111111111"
    payment_ussd_code = "*889*767*8972#"
    app_fee = 10

    httpretty.register_uri(
        httpretty.POST,
        "https://api.flutterwave.com/v3/charges?type=ussd",
        responses=[
            httpretty.core.httpretty.Response('{ "status": "error" }', status=400),
            httpretty.core.httpretty.Response('{ "status": "error" }', status=400),
            httpretty.core.httpretty.Response(
                create_charges_response(
                    tx_ref=start_request.tx_ref,
                    amount=start_request.amount,
                    app_fee=app_fee,
                    customer_phone=start_request.customer_phone,
                    customer_email=start_request.customer_email,
                    customer_name=start_request.customer_name,
                    currency=start_request.currency,
                    payment_code=payment_code,
                    fw_transaction_id=fw_transaction_id,
                    flw_ref=flw_ref,
                    payment_ussd_code=payment_ussd_code,
                ),
                status=200,
            ),
        ],
    )

    # Act
    resp = client.start_ussd_payment(request=start_request)

    # Assert
    assert json.loads(httpretty.last_request().body) == {
        "tx_ref": start_request.tx_ref,
        "account_bank": start_request.account_bank,
        "amount": start_request.amount,
        "currency": start_request.currency,
        "email": start_request.customer_email,
        "phone_number": start_request.customer_phone,
        "fullname": start_request.customer_name,
        "meta": {
            "customer_id": start_request.customer_id,
        },
    }

    assert resp.payment_code == payment_code
    assert resp.ussd_code == payment_ussd_code
    assert resp.transaction == FwTransaction(
        tx_ref=start_request.tx_ref,
        currency=start_request.currency,
        amount=start_request.amount,
        app_fee=app_fee,
        merchant_fee=0.0,
        charged_amount=start_request.amount + app_fee,
        amount_settled=None,
        customer_id=start_request.customer_id,
        customer_email=start_request.customer_email,
        customer_name=start_request.customer_name,
        customer_phone=start_request.customer_phone,
        status=FwTransactionStatus.PENDING,
        created_at=datetime(2021, 12, 20, 10, 14, 9, 0, tzinfo=timezone.utc),
        flw_ref=flw_ref,
        payment_type=FwPaymentType.USSD.value,
        transaction_id=fw_transaction_id,
    )


def test_integration_create_ussd_transaction_and_get_status_succeeds():

    secret_key = os.getenv("INTEGRATION_TESTS_FLUTTERWAVE_SECRET_KEY")
    if not secret_key:
        pytest.skip("No secret key provided")

    # Arrange
    client = FlutterWaveClient(secret_key=secret_key)

    start_request = create_start_ussd_request()

    # Act
    start_payment_resp = client.start_ussd_payment(request=start_request)

    # Assert
    assert len(start_payment_resp.payment_code) > 0
    assert len(start_payment_resp.ussd_code) > 0

    resp_tx = start_payment_resp.transaction
    assert resp_tx.tx_ref == start_request.tx_ref
    assert resp_tx.customer_id == start_request.customer_id
    assert resp_tx.currency == start_request.currency
    assert resp_tx.amount == start_request.amount
    assert len(resp_tx.flw_ref) > 0
    assert resp_tx.payment_type == FwPaymentType.USSD.value

    get_payment_resp = client.get_transaction_status(
        start_payment_resp.transaction.transaction_id
    )
    assert get_payment_resp.currency == start_request.currency
    assert get_payment_resp.amount == start_request.amount
    assert get_payment_resp.customer_id == start_request.customer_id
    assert get_payment_resp.customer_email == start_request.customer_email
    assert get_payment_resp.customer_name == start_request.customer_name
    assert get_payment_resp.customer_phone == start_request.customer_phone
    assert get_payment_resp.tx_ref == start_request.tx_ref
    assert get_payment_resp.payment_type == FwPaymentType.USSD.value
    assert get_payment_resp.transaction_id == resp_tx.transaction_id
    assert get_payment_resp.flw_ref == resp_tx.flw_ref
    assert get_payment_resp.status in [
        FwTransactionStatus.PENDING,
        FwTransactionStatus.SUCCESSFUL,
    ]


@mock.patch("requests.Session.post")
def test_create_ussd_transaction_timeout(post_mock, caplog):
    # Arrange
    test_secret_key = "secret"
    client = FlutterWaveClient(secret_key=test_secret_key)

    start_request = create_start_ussd_request()

    post_mock.side_effect = requests.Timeout

    # Act and Assert
    with caplog.at_level(logging.ERROR):

        with pytest.raises(Timeout):
            _ = client.start_ussd_payment(request=start_request)

        assert "USSD transaction timed out" in caplog.text
        assert "Timeout" in caplog.text
