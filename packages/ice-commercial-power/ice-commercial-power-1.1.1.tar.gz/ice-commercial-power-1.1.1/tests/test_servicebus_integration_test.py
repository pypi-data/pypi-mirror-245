"""
Integration Tests for Service Bus.
Only enabled if the following environment variables are set:
- INTEGRATION_TEST_SERVICEBUS_CONNECTION_STRING
- INTEGRATION_TEST_SERVICEBUS_QUEUE_NAME
- INTEGRATION_TEST_SERVICEBUS_TOPIC_NAME
- INTEGRATION_TEST_SERVICEBUS_TOPIC_SUBSCRIPTION_NAME
"""
# pylint: disable=redefined-outer-name

import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
import pytest

from azure.identity import DefaultAzureCredential
import azure.servicebus as sb
import icecommercialpower.messaging.servicebus as managed_servicebus


@dataclass
class TestSettings:
    """Settings for the integration tests."""

    connection_string: str
    queue_name: str
    topic_name: str
    topic_subscription_name: str

    def skip_if_empty(self) -> None:
        """Skip the test if any of the settings are empty."""
        if (
            not self.connection_string
            or not self.queue_name
            or not self.topic_name
            or not self.topic_subscription_name
        ):
            pytest.skip("Skipping integration test. Environment variables not set.")


@pytest.fixture(scope="session")
def test_settings() -> TestSettings:
    """Returns the test settings."""
    return TestSettings(
        connection_string=os.getenv("INTEGRATION_TEST_SERVICEBUS_CONNECTION_STRING"),
        queue_name=os.getenv("INTEGRATION_TEST_SERVICEBUS_QUEUE_NAME"),
        topic_name=os.getenv("INTEGRATION_TEST_SERVICEBUS_TOPIC_NAME"),
        topic_subscription_name=os.getenv(
            "INTEGRATION_TEST_SERVICEBUS_TOPIC_SUBSCRIPTION_NAME"
        ),
    )


# Use this to use a service principal for testing purposes.
# @pytest.fixture(autouse=True)
# def setup_sp(monkeypatch: pytest.MonkeyPatch) -> None:
#     monkeypatch.setenv("AZURE_TENANT_ID", "")
#     monkeypatch.setenv("AZURE_CLIENT_ID", "")
#     monkeypatch.setenv("AZURE_CLIENT_SECRET", "")


# pylint: disable=protected-access
@pytest.fixture(autouse=True)
def reset_service_bus_cache():
    """Clear the cache between tests"""
    managed_servicebus._get_service_bus_client.cache_clear()
    managed_servicebus._get_queue_sender.cache_clear()
    managed_servicebus._get_topic_sender.cache_clear()


def resolve_service_bus_client(
    use_managed_identity: bool, connection_string: str
) -> sb.ServiceBusClient:
    """Resolves a Service Bus client."""
    if use_managed_identity:
        return sb.ServiceBusClient(
            fully_qualified_namespace=sb.parse_connection_string(
                connection_string
            ).fully_qualified_namespace,
            credential=DefaultAzureCredential(),
        )
    return sb.ServiceBusClient.from_connection_string(connection_string)


@pytest.mark.parametrize(
    "use_managed_identity",
    [True, False],
    ids=["with managed identity", "with connection string"],
)
def test_send_queue_message(
    test_settings: TestSettings,
    monkeypatch: pytest.MonkeyPatch,
    use_managed_identity: bool,
):
    """
    Test sending a message to a Service Bus Queue.
    """
    test_settings.skip_if_empty()

    if use_managed_identity:
        monkeypatch.setenv(managed_servicebus.MANAGED_IDENTITY_SETTING_NAME, "1")

    message_ids = [str(uuid.uuid4()) for _ in range(5)]

    for message_id in message_ids:
        managed_servicebus.send_queue_message(
            connection_string=test_settings.connection_string,
            queue_name=test_settings.queue_name,
            message=sb.ServiceBusMessage(
                body="integration test", message_id=message_id
            ),
        )

    expected_message_ids = set(message_ids)

    sb_client = resolve_service_bus_client(
        use_managed_identity, test_settings.connection_string
    )
    with sb_client.get_queue_receiver(
        test_settings.queue_name, max_wait_time=30
    ) as receiver:
        for msg in receiver:  # type: ServiceBusMessage

            if msg.message_id in expected_message_ids:
                expected_message_ids.remove(msg.message_id)

            receiver.complete_message(msg)

            if len(expected_message_ids) == 0:
                break

    assert (
        len(expected_message_ids) == 0
    ), f"Didn't receive messages {expected_message_ids} in queue {test_settings.queue_name}."


@pytest.mark.parametrize(
    "use_managed_identity",
    [True, False],
    ids=["with managed identity", "with connection string"],
)
def test_send_scheduled_queue_message(
    test_settings: TestSettings,
    monkeypatch: pytest.MonkeyPatch,
    use_managed_identity: bool,
):
    """
    Test sending a scheduled message to a Service Bus Queue.
    """
    test_settings.skip_if_empty()

    if use_managed_identity:
        monkeypatch.setenv(managed_servicebus.MANAGED_IDENTITY_SETTING_NAME, "1")

    message_id = str(uuid.uuid4())
    managed_servicebus.schedule_queue_message(
        connection_string=test_settings.connection_string,
        queue_name=test_settings.queue_name,
        message=sb.ServiceBusMessage(body="integration test", message_id=message_id),
        schedule_time_utc=datetime.utcnow() + timedelta(seconds=5),
    )

    sb_client = resolve_service_bus_client(
        use_managed_identity, test_settings.connection_string
    )
    found_message = False
    with sb_client.get_queue_receiver(
        test_settings.queue_name, max_wait_time=30
    ) as receiver:
        for msg in receiver:  # type: ServiceBusMessage
            receiver.complete_message(msg)
            if msg.message_id == message_id:
                found_message = True
                break

    assert (
        found_message
    ), f"Didn't receive scheduled message {message_id} in queue {test_settings.queue_name}."


@pytest.mark.parametrize(
    "use_managed_identity",
    [True, False],
    ids=["with managed identity", "with connection string"],
)
def test_send_topic_message(
    test_settings: TestSettings,
    monkeypatch: pytest.MonkeyPatch,
    use_managed_identity: bool,
):
    """
    Test sending a message to a Service Bus Topic.
    """
    test_settings.skip_if_empty()

    if use_managed_identity:
        monkeypatch.setenv(managed_servicebus.MANAGED_IDENTITY_SETTING_NAME, "1")

    message_ids = [str(uuid.uuid4()) for _ in range(5)]

    for message_id in message_ids:
        managed_servicebus.send_topic_message(
            connection_string=test_settings.connection_string,
            topic_name=test_settings.topic_name,
            message=sb.ServiceBusMessage(
                body="integration test", message_id=message_id
            ),
        )

    expected_message_ids = set(message_ids)

    sb_client = resolve_service_bus_client(
        use_managed_identity, test_settings.connection_string
    )
    with sb_client.get_subscription_receiver(
        test_settings.topic_name,
        test_settings.topic_subscription_name,
        max_wait_time=30,
    ) as receiver:
        for msg in receiver:  # type: ServiceBusMessage

            if msg.message_id in expected_message_ids:
                expected_message_ids.remove(msg.message_id)

            receiver.complete_message(msg)

            if len(expected_message_ids) == 0:
                break

    assert len(expected_message_ids) == 0, (
        f"Missing messages {expected_message_ids} from {test_settings.topic_name}"
        "/{test_settings.topic_subscription_name}."
    )
