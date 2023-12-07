"""Tests of service_bus helpers"""
# pylint: disable=redefined-outer-name

from datetime import datetime
from unittest.mock import MagicMock, call, patch
import pytest
from pytest import MonkeyPatch

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusMessage, ServiceBusSender, ServiceBusClient
import icecommercialpower.messaging.servicebus as managed_servicebus


# pylint: disable=protected-access
@pytest.fixture(autouse=True)
def reset_service_bus_cache():
    """Clear the cache between tests"""
    managed_servicebus._get_queue_sender.cache_clear()
    managed_servicebus._get_service_bus_client.cache_clear()
    managed_servicebus._get_topic_sender.cache_clear()


@pytest.fixture
def service_bus_client():
    """Setups the ServiceBusClient mock returned by from_connection_string"""
    client = MagicMock(spec=ServiceBusClient)
    return client


@pytest.fixture
def service_bus_from_env(
    service_bus_client: MagicMock, monkeypatch: MonkeyPatch
) -> MagicMock:
    """Setups the ServiceBusClient.from_connection_string"""
    from_connection_string_mock = MagicMock(return_value=service_bus_client)
    monkeypatch.setattr(
        "azure.servicebus.ServiceBusClient.from_connection_string",
        from_connection_string_mock,
    )
    return from_connection_string_mock


@pytest.mark.parametrize("connection_string", [None, ""], ids=["None", "Empty"])
def test_send_without_connection_string(connection_string: str):
    """Test that ValueError is raised when connection_string is None or empty"""
    sb_message = ServiceBusMessage("test")

    with pytest.raises(ValueError):
        managed_servicebus.send_queue_message(connection_string, "my_queue", sb_message)

    with pytest.raises(ValueError):
        managed_servicebus.send_topic_message(connection_string, "my_topic", sb_message)

    with pytest.raises(ValueError):
        managed_servicebus.schedule_queue_message(
            connection_string, "my_queue", sb_message, datetime.utcnow()
        )


@pytest.mark.parametrize("queue_or_topic_name", [None, ""], ids=["None", "Empty"])
def test_send_without_queue_name(queue_or_topic_name: str):
    """Test that send_queue_message raises ValueError when queue_nanme is None or empty"""
    sb_message = ServiceBusMessage("test")

    with pytest.raises(ValueError):
        managed_servicebus.send_queue_message(
            "my_connection_string", queue_or_topic_name, sb_message
        )

    with pytest.raises(ValueError):
        managed_servicebus.send_topic_message(
            "my_connection_string", queue_or_topic_name, sb_message
        )

    with pytest.raises(ValueError):
        managed_servicebus.schedule_queue_message(
            "my_connection_string", queue_or_topic_name, sb_message, datetime.utcnow()
        )


def test_queue_send_reuses_same_client_and_sender(
    service_bus_from_env: MagicMock, service_bus_client: MagicMock
):
    """Test that send_queue_message reuses the same client and sender"""
    # Arrange
    queue_sender = MagicMock(spec=ServiceBusSender)
    service_bus_client.get_queue_sender.return_value = queue_sender

    # Act
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue",
        message=ServiceBusMessage("test1"),
    )
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue",
        message=ServiceBusMessage("test2"),
    )
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue",
        message=ServiceBusMessage("test3"),
    )

    # Assert
    service_bus_from_env.assert_called_once_with("my_connection_string")
    service_bus_client.get_queue_sender.assert_called_once_with("my_queue")
    assert queue_sender.send_messages.call_count == 3


def test_queue_send_reuses_same_client(
    service_bus_from_env: MagicMock, service_bus_client: MagicMock
):
    """Test that send_queue_message reuses the same client"""
    # Arrange
    queue_senders = [MagicMock(spec=ServiceBusSender) for _ in range(3)]
    service_bus_client.get_queue_sender.side_effect = queue_senders

    # Act
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue_1",
        message=ServiceBusMessage("test1"),
    )
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue_2",
        message=ServiceBusMessage("test2"),
    )
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string",
        queue_name="my_queue_3",
        message=ServiceBusMessage("test3"),
    )

    # Assert
    service_bus_from_env.assert_called_once_with("my_connection_string")
    assert service_bus_client.get_queue_sender.call_count == 3
    service_bus_client.get_queue_sender.assert_has_calls(
        [call("my_queue_1"), call("my_queue_2"), call("my_queue_3")], any_order=True
    )

    for index, sender in enumerate(queue_senders):
        sender.send_messages.assert_called_once()
        [[msg], _] = sender.send_messages.call_args
        assert list(msg.body)[0].decode("utf-8") == f"test{index + 1}"


def test_queue_send_different_connection_strings(service_bus_from_env: MagicMock):
    """Test that send_queue_message creates different client per connection string"""
    # Arrange
    service_bus_client_1 = MagicMock(spec=ServiceBusClient)
    service_bus_client_2 = MagicMock(spec=ServiceBusClient)
    service_bus_from_env.side_effect = [service_bus_client_1, service_bus_client_2]

    service_bus_client_1.get_queue_sender.return_value = MagicMock(
        spec=ServiceBusSender
    )
    service_bus_client_2.get_queue_sender.return_value = MagicMock(
        spec=ServiceBusSender
    )

    # Act
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string_1",
        queue_name="my_queue",
        message=ServiceBusMessage("connection_string_1_test"),
    )
    managed_servicebus.send_queue_message(
        connection_string="my_connection_string_2",
        queue_name="my_queue",
        message=ServiceBusMessage("connection_string_2_test"),
    )

    # Assert
    assert (
        service_bus_from_env.call_count == 2
    ), "Should have called from_connection_string twice"

    for index, service_bus_client in enumerate(
        [service_bus_client_1, service_bus_client_2]
    ):
        service_bus_client.get_queue_sender.assert_called_once()
        service_bus_client.get_queue_sender.return_value.send_messages.assert_called_once()
        [
            [msg],
            _,
        ] = service_bus_client.get_queue_sender.return_value.send_messages.call_args
        assert (
            list(msg.body)[0].decode("utf-8") == f"connection_string_{index + 1}_test"
        )


def test_topic_send_reuses_same_client_and_sender(
    service_bus_from_env: MagicMock, service_bus_client: MagicMock
):
    """Test that send_topic_message reuses the same client and sender"""
    # Arrange
    topic_sender = MagicMock(spec=ServiceBusSender)
    service_bus_client.get_topic_sender.return_value = topic_sender

    # Act
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic",
        message=ServiceBusMessage("test1"),
    )
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic",
        message=ServiceBusMessage("test2"),
    )
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic",
        message=ServiceBusMessage("test3"),
    )

    # Assert
    service_bus_from_env.assert_called_once_with("my_connection_string")
    service_bus_client.get_topic_sender.assert_called_once_with("my_topic")
    assert topic_sender.send_messages.call_count == 3


def test_topic_send_reuses_same_client(
    service_bus_from_env: MagicMock, service_bus_client: MagicMock
):
    """Test that send_topic_message reuses the same client"""
    # Arrange
    topic_senders = [MagicMock(spec=ServiceBusSender) for _ in range(3)]
    service_bus_client.get_topic_sender.side_effect = topic_senders

    # Act
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic_1",
        message=ServiceBusMessage("test1"),
    )
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic_2",
        message=ServiceBusMessage("test2"),
    )
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string",
        topic_name="my_topic_3",
        message=ServiceBusMessage("test3"),
    )

    # Assert
    service_bus_from_env.assert_called_once_with("my_connection_string")
    assert service_bus_client.get_topic_sender.call_count == 3
    service_bus_client.get_topic_sender.assert_has_calls(
        [call("my_topic_1"), call("my_topic_2"), call("my_topic_3")], any_order=True
    )

    for index, sender in enumerate(topic_senders):
        sender.send_messages.assert_called_once()
        [[msg], _] = sender.send_messages.call_args
        assert list(msg.body)[0].decode("utf-8") == f"test{index + 1}"


def test_topic_send_different_connection_strings(service_bus_from_env: MagicMock):
    """Test that send_topic_message creates different client per connection string"""
    # Arrange
    service_bus_client_1 = MagicMock(spec=ServiceBusClient)
    service_bus_client_2 = MagicMock(spec=ServiceBusClient)
    service_bus_from_env.side_effect = [service_bus_client_1, service_bus_client_2]

    service_bus_client_1.get_topic_sender.return_value = MagicMock(
        spec=ServiceBusSender
    )
    service_bus_client_2.get_topic_sender.return_value = MagicMock(
        spec=ServiceBusSender
    )

    # Act
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string_1",
        topic_name="my_topic",
        message=ServiceBusMessage("connection_string_1_test"),
    )
    managed_servicebus.send_topic_message(
        connection_string="my_connection_string_2",
        topic_name="my_topic",
        message=ServiceBusMessage("connection_string_2_test"),
    )

    # Assert
    assert (
        service_bus_from_env.call_count == 2
    ), "Should have called from_connection_string twice"

    for index, service_bus_client in enumerate(
        [service_bus_client_1, service_bus_client_2]
    ):
        service_bus_client.get_topic_sender.assert_called_once()
        service_bus_client.get_topic_sender.return_value.send_messages.assert_called_once()
        [
            [msg],
            _,
        ] = service_bus_client.get_topic_sender.return_value.send_messages.call_args
        assert (
            list(msg.body)[0].decode("utf-8") == f"connection_string_{index + 1}_test"
        )


@pytest.mark.parametrize(
    "connection_string",
    [
        "Endpoint=sb://testing.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=aaabbbccc",  # pylint: disable=line-too-long
        "testing.servicebus.windows.net",
    ],
)
def test_create_service_bus_for_managed_identity(
    connection_string: str, monkeypatch: pytest.MonkeyPatch
):
    """Test that once enabled, we create the service bus client using azure credentials"""

    # Arrange
    monkeypatch.setenv(managed_servicebus.MANAGED_IDENTITY_SETTING_NAME, "1")
    servicebus_client_instance = MagicMock(spec=ServiceBusClient)

    # Act
    # As we patch the constructor, we need to use the package name:
    # https://stackoverflow.com/questions/57042557/pytest-mocking-constructor-within-constructor
    with patch(
        "icecommercialpower.messaging.servicebus.ServiceBusClient",
        spec=ServiceBusClient,
    ) as servicebus_client:
        servicebus_client.return_value = servicebus_client_instance
        managed_servicebus.send_queue_message(
            connection_string=connection_string,
            queue_name="my_queue",
            message=ServiceBusMessage("test1"),
        )

    # Assert
    servicebus_client.from_connection_string.assert_not_called()
    servicebus_client.assert_called_once()
    assert (
        servicebus_client.call_args.kwargs["fully_qualified_namespace"]
        == "testing.servicebus.windows.net"
    )
    assert isinstance(
        servicebus_client.call_args.kwargs["credential"], DefaultAzureCredential
    )
    servicebus_client_instance.get_queue_sender.assert_called_once()


def test_create_service_bus_for_connection_strings():
    """Test that once enabled, we create the service bus client using connection strings"""

    # Arrange

    # Act
    # As we patch the constructor, we need to use the package name:
    # https://stackoverflow.com/questions/57042557/pytest-mocking-constructor-within-constructor
    with patch(
        "icecommercialpower.messaging.servicebus.ServiceBusClient",
        spec=ServiceBusClient,
    ) as servicebus_client:
        managed_servicebus.send_queue_message(
            connection_string="my_connection_string",
            queue_name="my_queue",
            message=ServiceBusMessage("test1"),
        )

    # Assert
    servicebus_client.from_connection_string.assert_called_once_with(
        "my_connection_string"
    )
