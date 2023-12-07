"""PaymentRepository tests"""
from datetime import datetime
import uuid
from unittest.mock import MagicMock, patch
import pytest
from azure.cosmos.exceptions import (
    CosmosResourceExistsError,
    CosmosAccessConditionFailedError,
)
from icecommercialpower.payments import (
    PaymentRepository,
    Payment,
    PaymentStatus,
    NotificationStatus,
)
from .cosmos_testing_utils import create_test_container, try_create_cosmos_client


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def payment_repository() -> PaymentRepository:
    """
    Try to create the repository
    """
    client = try_create_cosmos_client()
    if not client:
        return None

    database_name = "test_db"
    create_test_container(
        client=client,
        db_name=database_name,
        container_name=PaymentRepository.Config.ContainerName,
        partition_key_path="/customer_id",
    )

    return PaymentRepository(client, database_name)


def create_test_payment() -> Payment:
    """Creates test payment"""
    return Payment(
        id=str(uuid.uuid4()),
        date_created=datetime.utcnow(),
        customer_id=100,
        customer_name="Ana testing",
        customer_email="ana@testing.com",
        customer_phone_number="123456789",
        amount=100,
        currency="NGN",
        external_id="12345",
        external_ref="REF#12345",
        status=PaymentStatus.PENDING,
        notification=NotificationStatus.NOT_STARTED,
    )


def test_create_or_update_not_allowed():
    """Not allowed: Create or update a payment"""
    with pytest.raises(NotImplementedError):
        PaymentRepository(MagicMock(), "payments").create_or_update(
            create_test_payment()
        )


def test_create_payment(payment_repository: PaymentRepository):
    """Create a payment"""
    if not payment_repository:
        pytest.skip("Integration test connection string not set")

    # Arrange
    payment = create_test_payment()

    # Act
    created = payment_repository.create(payment)

    # Assert
    loaded = payment_repository.get_payment(payment.id, payment.customer_id)

    assert created == loaded
    assert len(loaded.etag) > 0
    assert len(created.etag) > 0


def test_create_existing_payment(payment_repository: PaymentRepository):
    """Create an existing payment"""
    if not payment_repository:
        pytest.skip("Integration test connection string not set")

    # Arrange
    payment = create_test_payment()

    # Act
    payment_repository.create(payment)

    # Assert
    with pytest.raises(CosmosResourceExistsError):
        payment_repository.create(payment)


def test_update_optimistic_locking_fails(payment_repository: PaymentRepository):
    """Create an existing payment"""
    if not payment_repository:
        pytest.skip("Integration test connection string not set")

    # Arrange
    payment = payment_repository.create(create_test_payment())
    payment.etag = "Bad etag"

    # Act & Assert
    with pytest.raises(CosmosAccessConditionFailedError):
        payment_repository.update(payment)


def test_update_optimistic_locking_succeeds(payment_repository: PaymentRepository):
    """Create an existing payment"""
    if not payment_repository:
        pytest.skip("Integration test connection string not set")

    # Arrange
    payment = payment_repository.create(create_test_payment())
    payment.external_ref = payment.external_ref + "#Modified"

    # Act
    updated = payment_repository.update(payment)
    read = payment_repository.get_payment(payment.id, payment.customer_id)

    # Assert
    assert updated.external_ref == payment.external_ref
    assert updated.etag != payment.etag
    assert read.etag == updated.etag


@patch("azure.cosmos.CosmosClient.from_connection_string")
def test_from_env(
    cosmos_from_connection_string_mock: MagicMock, monkeypatch: pytest.MonkeyPatch
):
    """Create a payment repository from environment variables"""

    # Arrange
    cosmos_client = MagicMock()
    cosmos_from_connection_string_mock.return_value = cosmos_client
    cosmos_connection_string = "my-connection-string"
    monkeypatch.setenv("COSMOSDB_CONNECTION_STRING", cosmos_connection_string)

    # Act & Assert
    assert PaymentRepository.from_env() is not None

    cosmos_from_connection_string_mock.assert_called_once_with(cosmos_connection_string)
