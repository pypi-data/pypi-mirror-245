"""
Integration Tests for the BaseRepository
Requires setting the environment variable: INTEGRATION_TESTS_COSMOS_DB_CONNECT_STRING
with a valid connection string for a Cosmos DB account

Options:
- Using Cosmos DB emulator:
    https://docs.microsoft.com/azure/cosmos-db/local-emulator?tabs=ssl-netstd21
- Using a real Cosmos DB account: Create it in Azure (it has costs)
"""
# pylint: disable=redefined-outer-name,duplicate-code
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic.main import BaseModel
import pytest
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import (
    CosmosResourceNotFoundError,
    CosmosResourceExistsError,
)
from icecommercialpower.db import BaseRepository
from .cosmos_testing_utils import create_test_container, try_create_cosmos_client


class Car(BaseModel):
    """Car sample model"""

    id: str
    name: str
    purchase_date: datetime
    car_type: Optional[str]
    doc_type: str = "car"  # partition key for this entity


class CarRepository(BaseRepository):
    """Test repository with a single partition"""

    # pylint: disable=too-few-public-methods
    class Config:
        """Repository Config"""

        PartitionValue = "car"
        PartitionPath = "doc_type"
        ContainerName = "cars"
        Model = Car

    # pylint: disable=duplicate-code
    def __init__(self, client: CosmosClient) -> None:
        # For testing we create the database if needed
        db_name = "test_db"
        create_test_container(
            container_name=CarRepository.Config.ContainerName,
            partition_key_path=f"/{CarRepository.Config.PartitionPath}",
            included_index_paths=[{"path": "/car_type/?"}],
            client=client,
            db_name=db_name,
        )
        super().__init__(client, db_name)


@pytest.fixture(scope="module")
def repository() -> CarRepository:
    """Creates repository for testing"""
    client = try_create_cosmos_client()
    return CarRepository(client) if client else None


def create_test_car(
    car_id: str = None,
    name: str = None,
    purchase_date: datetime = None,
    car_type: str = None,
) -> Car:
    """Creates a test car"""
    car_id = car_id if car_id is not None else str(uuid.uuid4())
    name = name if name is not None else "Audi"
    purchase_date = (
        purchase_date if purchase_date else datetime.utcnow() - timedelta(days=5 * 365)
    )

    return Car(id=car_id, name=name, purchase_date=purchase_date, car_type=car_type)


def test_fix_partition_create_and_read_item(repository: CarRepository):
    """Test create and read item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    original_car = create_test_car()

    repository.create_or_update(original_car)

    loaded_car = repository.get(original_car.id)

    assert original_car == loaded_car


def test_fix_partition_update_and_read_item(repository: CarRepository):
    """Test update and read item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    original_car = create_test_car()

    repository.create_or_update(original_car)

    modified_car = create_test_car(
        car_id=original_car.id,
        purchase_date=datetime(year=2020, month=1, day=25),
        car_type="Sedan",
    )

    repository.create_or_update(modified_car)

    loaded_car = repository.get(original_car.id)

    assert modified_car == loaded_car


def test_fix_partition_get_non_existing_item(repository: CarRepository):
    """Test get non existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car_id = str(uuid.uuid4())

    loaded_car = repository.get(car_id)

    # Assert
    assert loaded_car is None


def test_fix_partition_query_non_existing_items(repository: CarRepository):
    """Test query non existing items"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    actual = repository.query(
        query="SELECT * FROM c WHERE c.name = @name",
        parameters=[{"name": "@name", "value": str(uuid.uuid4())}],
    )

    assert len(actual) == 0


def test_fix_partition_query_existing_items(repository: CarRepository):
    """Test query existing items"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    car_type = str(uuid.uuid4())

    expected_cars_count = 10

    cars: List[Car] = []
    for _ in range(expected_cars_count):
        car = create_test_car(car_type=car_type)

        repository.create_or_update(car)
        cars.append(car)

    # Act
    actual = repository.query(
        query="SELECT * FROM c WHERE c.car_type = @car_type",
        parameters=[{"name": "@car_type", "value": car_type}],
    )

    # Assert
    assert cars == actual


def test_fix_partition_update_non_existing_item(repository: CarRepository):
    """Test update non existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car = create_test_car()

    with pytest.raises(CosmosResourceNotFoundError):
        repository.update(car)


def test_fix_partition_update_existing_item(repository: CarRepository):
    """Test update existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car = create_test_car()

    repository.create_or_update(car)

    modified_car = Car(
        id=car.id, name="Mercedes", purchase_date=datetime(year=2020, month=1, day=25)
    )

    repository.update(modified_car)
    loaded_car = repository.get(car.id)

    # Assert
    assert loaded_car == modified_car


def test_fix_partition_create_new_item(repository: CarRepository):
    """Test create new item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car = create_test_car()

    repository.create(car)

    loaded_car = repository.get(car.id)

    # Assert
    assert loaded_car == car


def test_fix_partition_create_existing_item(repository: CarRepository):
    """Test create existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car = create_test_car()

    repository.create(car)

    # Assert
    with pytest.raises(CosmosResourceExistsError):
        repository.create(car)


def test_fix_partition_delete_existing_item(repository: CarRepository):
    """Test delete existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    car = create_test_car()

    repository.create(car)

    loaded = repository.get(car.id)
    assert loaded == car

    repository.delete(car.id)
    assert repository.get(car.id) is None


def test_fix_partition_delete_non_existing_item(repository: CarRepository):
    """Test delete existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    with pytest.raises(CosmosResourceNotFoundError):
        repository.delete(str(uuid.uuid4()))
