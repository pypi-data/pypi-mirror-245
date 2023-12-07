"""
Tests for Stemaco client customer transactions.
"""

import os
import uuid
import requests
import httpretty
import pytest

from icecommercialpower.steamaco import (
    TransactionCategory,
    TransactionProvider,
    Transaction,
    CreateTransactionError,
    SteamaCoClient,
)

from .steamaco_test_utils import (
    setup_steamaco_env_vars,
    create_list_response,
    register_auth_request,
)


CUSTOMER_ID = 1
TRANSACTION_REFERENCE = "ABC123"
TRANSACTION_ID = 1000
TRANSACTION_AMOUNT = float(2000)
CURRENCY = "NGN"


@pytest.fixture(autouse=True)
def setup_function(monkeypatch):
    """
    Setup function for the steamaco tests
    """
    # pylint: disable=protected-access
    SteamaCoClient._cached_token.reset()

    setup_steamaco_env_vars(monkeypatch)


def get_customer_transactions_url(
    customer_id: int = CUSTOMER_ID, reference: str = TRANSACTION_REFERENCE
) -> str:
    """
    Get customer transactions url
    """
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_customers_url = os.environ["STEAMACO_CUSTOMERS_URL"]
    steamaco_customer_transactions_url = (
        f"{steamaco_api_url}{steamaco_customers_url}{customer_id}/transactions/"
    )

    if reference:
        return (
            f"{steamaco_customer_transactions_url}"
            f"?reference={reference}"
            f"&{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
        )

    return (
        f"{steamaco_customer_transactions_url}"
        f"?{SteamaCoClient.PAGE_SIZE_PARAM_NAME}={SteamaCoClient.DEFAULT_PAGE_SIZE}"
    )


def create_customer_transactions_url(customer_id: int = CUSTOMER_ID) -> str:
    """
    Helper to create a customer transactions url
    """
    steamaco_api_url = os.environ["STEAMACO_API_URL"]
    steamaco_customers_url = os.environ["STEAMACO_CUSTOMERS_URL"]

    return f"{steamaco_api_url}{steamaco_customers_url}{customer_id}/transactions/"


def create_transaction_json(
    customer_id: int = CUSTOMER_ID,
    transaction_id: int = TRANSACTION_ID,
    reference: str = TRANSACTION_REFERENCE,
    amount: float = TRANSACTION_AMOUNT,
) -> str:
    """
    Helper to create a transaction json
    """
    return f""" {{
        "id": {transaction_id},
        "url": "https://api.steama.co/transactions/{transaction_id}/",
        "timestamp": "2021-11-29T16:05:21Z",
        "amount": "{amount}",
        "category": "PAY",
        "reference": "{reference}",
        "raw_message": "",
        "account_balance": "{amount + 100}",
        "provider": "AP",
        "customer_url": "https://api.steama.co/customers/{customer_id}/",
        "customer_id": {customer_id},
        "customer_first_name": "John",
        "customer_last_name": "Testing",
        "customer_telephone": "+123456798",
        "agent_url": null,
        "agent_id": null,
        "agent_first_name": null,
        "agent_last_name": null,
        "agent_telephone": null,
        "user": 1000,
        "username": "testing_user",
        "reversed_by_id": null,
        "reversed_by_url": null,
        "reversed_by_reference": null,
        "currency": "{CURRENCY}",
        "currency_display": "NgN",
        "synchronization_status": "N/A"
    }}"""


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("reference", [TRANSACTION_REFERENCE, None])
def test_get_customer_transactions_empty(reference: str):
    """
    Test for empty steamaco_get_customer_transactions
    """

    # Arrange
    httpretty.enable()
    register_auth_request()

    httpretty.register_uri(
        method=httpretty.GET,
        uri=get_customer_transactions_url(1, reference),
        body=create_list_response(),
        content_type="application/json",
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()
    customer_transactions = steamaco_client.get_customer_transactions(
        CUSTOMER_ID, reference
    )

    # Assert
    assert len(customer_transactions) == 0


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("reference", [TRANSACTION_REFERENCE, None])
def test_get_customer_transactions_with_multiple_results(reference: str):
    """
    Test for multiple steamaco_get_customer_transactions returns
    """

    # Arrange
    httpretty.enable()
    register_auth_request()

    transaction_id_2 = 3000
    transaction_amount_2 = float(5000)
    transactions_response = create_list_response(
        results=f"[{create_transaction_json()},"
        f"{create_transaction_json(transaction_id=transaction_id_2, amount=transaction_amount_2)}]"
    )
    httpretty.register_uri(
        method=httpretty.GET,
        uri=get_customer_transactions_url(1, reference),
        body=transactions_response,
        content_type="application/json",
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()
    customer_transactions = steamaco_client.get_customer_transactions(
        CUSTOMER_ID, reference
    )

    # Assert
    assert len(customer_transactions) == 2

    customer_transaction_1 = customer_transactions[0]
    assert customer_transaction_1.id == TRANSACTION_ID
    assert customer_transaction_1.reference == TRANSACTION_REFERENCE
    assert float(customer_transaction_1.amount) == TRANSACTION_AMOUNT
    assert customer_transaction_1.customer_id == CUSTOMER_ID
    assert customer_transaction_1.provider == TransactionProvider.AP
    assert customer_transaction_1.category == TransactionCategory.PAY
    assert customer_transaction_1.currency == CURRENCY

    customer_transaction_2 = customer_transactions[1]
    assert customer_transaction_2.id == transaction_id_2
    assert customer_transaction_2.reference == TRANSACTION_REFERENCE
    assert float(customer_transaction_2.amount) == transaction_amount_2
    assert customer_transaction_2.customer_id == CUSTOMER_ID
    assert customer_transaction_2.provider == TransactionProvider.AP
    assert customer_transaction_2.category == TransactionCategory.PAY
    assert customer_transaction_2.currency == CURRENCY


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("reference", [TRANSACTION_REFERENCE, None])
def test_get_customer_transactions_single_result(reference: str):
    """
    Test for steamaco_get_customer_transactions return single element
    """

    # Arrange
    httpretty.enable()
    register_auth_request()

    transactions_response = create_list_response(
        results=f"[{create_transaction_json()}]"
    )
    httpretty.register_uri(
        method=httpretty.GET,
        uri=get_customer_transactions_url(1, reference),
        body=transactions_response,
        content_type="application/json",
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()
    customer_transactions = steamaco_client.get_customer_transactions(
        CUSTOMER_ID, reference
    )

    # Assert
    assert len(customer_transactions) == 1
    customer_transaction = customer_transactions[0]
    assert customer_transaction.id == TRANSACTION_ID
    assert customer_transaction.reference == TRANSACTION_REFERENCE
    assert float(customer_transaction.amount) == TRANSACTION_AMOUNT
    assert customer_transaction.customer_id == CUSTOMER_ID
    assert customer_transaction.provider == TransactionProvider.AP
    assert customer_transaction.category == TransactionCategory.PAY
    assert customer_transaction.currency == CURRENCY


@httpretty.activate(verbose=True, allow_net_connect=False)
@pytest.mark.parametrize("reference", [TRANSACTION_REFERENCE, None])
def test_get_customer_transactions_with_not_ok_status(reference: str):
    """
    Test getting customer transaction returning bad status
    """
    # Arrange
    httpretty.enable()
    register_auth_request()

    httpretty.register_uri(
        method=httpretty.GET,
        uri=get_customer_transactions_url(1, reference),
        body="{}",
        content_type="application/json",
        status=400,
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()

    with pytest.raises(requests.HTTPError):
        steamaco_client.get_customer_transactions(CUSTOMER_ID, reference)


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_customer_transactions_succeeded():
    """
    Test for steamaco_create_customer_transactions
    """
    # Arrange
    httpretty.enable()
    register_auth_request()

    transaction = Transaction.create(
        reference=str(uuid.uuid4()),
        amount=1000,
    )

    created_transaction = Transaction(
        id=TRANSACTION_ID,
        reference=transaction.reference,
        amount=transaction.amount,
        customer_id=CUSTOMER_ID,
        category=TransactionCategory.PAY,
        provider=TransactionProvider.AP,
    )

    httpretty.register_uri(
        method=httpretty.POST,
        uri=create_customer_transactions_url(CUSTOMER_ID),
        body=created_transaction.json(),
        content_type="application/json",
        status=201,
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()
    actual = steamaco_client.create_customer_transaction(CUSTOMER_ID, transaction)

    # Assert
    assert actual == created_transaction


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_create_customer_transactions_fails():
    """
    Test for steamaco_create_customer_transactions
    """
    # Arrange
    httpretty.enable()
    register_auth_request()

    transaction = Transaction.create(
        reference=str(uuid.uuid4()),
        amount=1000,
    )

    httpretty.register_uri(
        method=httpretty.POST,
        uri=create_customer_transactions_url(CUSTOMER_ID),
        body="{}",
        content_type="application/json",
        status=400,
        match_querystring=True,
    )

    # Act
    steamaco_client = SteamaCoClient()
    with pytest.raises(CreateTransactionError):
        steamaco_client.create_customer_transaction(CUSTOMER_ID, transaction)
