"""
Integration Tests for Stemaco client operations.
Only enabled if the following environment variables are set:
- INTEGRATION_TEST_STEAMACO_USERNAME
- INTEGRATION_TEST_STEAMACO_PASSWORD
- INTEGRATION_TEST_STEAMACO_CUSTOMER_ID
"""
# pylint: disable=redefined-outer-name

import os
import uuid
from _pytest.monkeypatch import monkeypatch
import pytest


from icecommercialpower.steamaco import (
    SteamaCoClient,
    Transaction,
    TransactionCategory,
    TransactionProvider,
)


@pytest.fixture()
def steamaco_client(monkeypatch: monkeypatch) -> SteamaCoClient:
    """Get a steamaco client instance."""
    test_username = os.getenv("INTEGRATION_TEST_STEAMACO_USERNAME")
    test_password = os.getenv("INTEGRATION_TEST_STEAMACO_PASSWORD")

    if not test_username or not test_password:
        return None

    monkeypatch.setenv("STEAMACO_USERNAME", test_username)
    monkeypatch.setenv("STEAMACO_PASSWORD", test_password)
    return SteamaCoClient()


@pytest.fixture()
def test_customer_id() -> int:
    """Gets the test customer id."""
    return int(os.getenv("INTEGRATION_TEST_STEAMACO_CUSTOMER_ID", "0"))


def test_get_customer_by_id(steamaco_client: SteamaCoClient, test_customer_id: int):
    """Test getting all a customer by identifier."""
    if not steamaco_client or not test_customer_id:
        pytest.skip("Integration test username, password or customer id not set")

    actual = steamaco_client.get_customer_by_id(customer_id=test_customer_id)
    assert actual is not None
    assert actual.id == test_customer_id
    assert len(actual.last_name) > 0
    assert len(actual.telephone) > 0


def test_integration_get_all_transactions(
    steamaco_client: SteamaCoClient, test_customer_id: int
):
    """
    Test getting all transactions for a given customer.
    """
    if not steamaco_client or not test_customer_id:
        pytest.skip("Integration test username, password or customer id not set")

    actual = steamaco_client.get_customer_transactions(customer_id=test_customer_id)
    assert len(actual) > 0


def test_integration_create_and_search_transactions(
    steamaco_client: SteamaCoClient, test_customer_id: int
):
    """
    Test creating a transaction and searching for it.
    """
    if not steamaco_client or not test_customer_id:
        pytest.skip("Integration test username, password or customer id not set")

    reference = str(uuid.uuid4())
    existing = steamaco_client.get_customer_transactions(
        customer_id=test_customer_id, reference=reference
    )
    assert len(existing) == 0

    transaction_amount = 100
    transaction = Transaction.create(
        amount=transaction_amount,
        reference=reference,
        raw_text="Integration test transaction",
    )

    created_transaction = steamaco_client.create_customer_transaction(
        customer_id=test_customer_id, transaction=transaction
    )
    assert created_transaction.reference == reference
    assert created_transaction.id > 0
    assert created_transaction.amount == transaction_amount
    assert created_transaction.customer_id == int(test_customer_id)
    assert created_transaction.category == TransactionCategory.PAY
    assert created_transaction.provider == TransactionProvider.AP

    loaded_created_transactions = steamaco_client.get_customer_transactions(
        customer_id=test_customer_id, reference=reference
    )
    assert len(loaded_created_transactions) == 1

    loaded_created_transaction = loaded_created_transactions[0]
    assert loaded_created_transaction.reference == reference
    assert loaded_created_transaction.id > 0
    assert loaded_created_transaction.amount == transaction_amount
    assert loaded_created_transaction.customer_id == int(test_customer_id)
    assert loaded_created_transaction.category == TransactionCategory.PAY
    assert loaded_created_transaction.provider == TransactionProvider.AP
