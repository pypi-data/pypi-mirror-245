"""BaseRepository tests"""
# pylint: disable=too-few-public-methods

from unittest.mock import MagicMock
import pytest
from icecommercialpower.db import BaseRepository


def test_invalid_cosmos_client():
    """
    Ensures that the client is valid
    """

    class TestRepositoryWithConfig(BaseRepository):
        """Test Repository"""

        class Config:
            """Repository Config"""

            Model = object
            ContainerName = "test_container"

        def __init__(self, client) -> None:
            super().__init__(client=client, db_name="test_db")

    with pytest.raises(ValueError):
        TestRepositoryWithConfig(client=None)


def test_missing_config():
    """
    Ensures that the config is defined
    """

    class TestRepository(BaseRepository):
        """Test Repository"""

        def __init__(self, client) -> None:
            super().__init__(client=client, db_name="test_db")

    with pytest.raises(NotImplementedError) as err:
        TestRepository(client=MagicMock())

    assert err.value.args[0] == "Config class is not defined."


def test_missing_model_in_config():
    """
    Ensures that the model is available
    """

    class TestRepositoryWithMissingModel(BaseRepository):
        """Test Repository"""

        class Config:
            """Repository Config"""

            ContainerName = "test_container"
            FixPartitionValue = "test"

        def __init__(self, client) -> None:
            super().__init__(client=client, db_name="test_db")

    with pytest.raises(NotImplementedError) as err:
        TestRepositoryWithMissingModel(client=MagicMock())

    assert err.value.args[0] == "Config must have a Model attribute."


def test_missing_container_name_in_config():
    """
    Ensures that the container name is available
    """

    class TestRepositoryWithMissingContainerName(BaseRepository):
        """Test Repository"""

        class Config:
            """Repository Config"""

            Model = object

        def __init__(self, client) -> None:
            super().__init__(client=client, db_name="test_db")

    with pytest.raises(NotImplementedError) as err:
        TestRepositoryWithMissingContainerName(client=MagicMock())

    assert err.value.args[0] == "Config must have a ContainerName attribute."


def test_query_cross_partition_enabled_with_partition_key():
    """
    Ensures that passing a partition key
    when querying with cross partition raises an error
    """

    class TestRepository(BaseRepository):
        """Test Repository"""

        class Config:
            """Repository Config"""

            Model = object
            ContainerName = "test_container"
            PartitionPath = "test"

        def __init__(self, client) -> None:
            super().__init__(client=client, db_name="test_db")

    repo = TestRepository(client=MagicMock())
    with pytest.raises(ValueError):
        repo.query(
            "SELECT c.* FROM c", enable_cross_partition_query=True, partition_key="foo"
        )
