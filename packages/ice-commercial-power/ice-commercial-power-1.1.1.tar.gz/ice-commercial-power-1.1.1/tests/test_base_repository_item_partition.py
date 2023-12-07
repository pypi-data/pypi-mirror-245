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


class Student(BaseModel):
    """Student sample model"""

    id: str
    first_name: str
    last_name: str
    school: str
    birth_date: datetime
    grade: Optional[int]


class StudentRepository(BaseRepository):
    """Test repository with a multiple partition"""

    # pylint: disable=too-few-public-methods
    class Config:
        """Repository Config"""

        ContainerName = "students"
        Model = Student

    # pylint: disable=duplicate-code
    def __init__(self, client: CosmosClient) -> None:
        # For testing we create the database if needed
        db_name = "test_db"
        create_test_container(
            container_name=StudentRepository.Config.ContainerName,
            partition_key_path="/school",
            included_index_paths=[{"path": "/last_name/?"}],
            client=client,
            db_name=db_name,
        )
        super().__init__(client, db_name)


@pytest.fixture(scope="module")
def repository() -> StudentRepository:
    """
    Try to create the repository
    """
    client = try_create_cosmos_client()
    return StudentRepository(client) if client else None


def create_test_student(
    student_id: str = None, last_name: str = None, school: str = None
) -> Student:
    """Create test student"""
    school = school if school is not None else str(uuid.uuid4())
    last_name = last_name if last_name else "Testing"
    student_id = student_id if student_id is not None else str(uuid.uuid4())
    return Student(
        id=student_id,
        first_name="John",
        last_name=last_name,
        school=school,
        birth_date=datetime.utcnow() - timedelta(days=20 * 365),
        grade=None,
    )


def test_create_and_read_item(repository: StudentRepository):
    """Test create and read item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    original = create_test_student()

    repository.create_or_update(original)

    loaded = repository.get(original.id, partition_key=original.school)

    assert original == loaded


def test_update_and_read_item(repository: StudentRepository):
    """Test update and read item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    original = create_test_student()

    repository.create_or_update(original)

    modified = create_test_student(
        student_id=original.id, last_name="Testing#Modified", school=original.school
    )

    repository.create_or_update(modified)

    loaded = repository.get(original.id, original.school)

    assert modified == loaded


def test_get_non_existing_item(repository: StudentRepository):
    """Test get non existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student_id = str(uuid.uuid4())
    partition_key = str(uuid.uuid4())
    loaded = repository.get(student_id, partition_key=partition_key)

    assert loaded is None


def test_get_non_existing_item_in_partition(repository: StudentRepository):
    """Test get non existing item in partition"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    original = create_test_student()
    repository.create(original)

    # Act
    partition_key = str(uuid.uuid4())
    loaded = repository.get(original.id, partition_key=partition_key)

    # Assert
    assert loaded is None


def test_query_single_partition_non_existing_items(repository: StudentRepository):
    """Test query single partition non existing items"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    partition_key = str(uuid.uuid4())
    actual = repository.query(
        query="SELECT * FROM c WHERE c.first_name = @first_name",
        parameters=[{"name": "@first_name", "value": "John"}],
        partition_key=partition_key,
    )

    assert len(actual) == 0


@pytest.mark.parametrize("same_partition", [True, False])
def test_query_existing_items(same_partition: bool, repository: StudentRepository):
    """Test query existing items"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")
    school = str(uuid.uuid4()) if same_partition else None

    expected_item_count = 10
    last_name = str(uuid.uuid4())
    items: List[Student] = []
    for _ in range(expected_item_count):
        item = create_test_student(school=school, last_name=last_name)

        repository.create_or_update(item)
        items.append(item)

    # Act
    actual = repository.query(
        query="SELECT * FROM c WHERE c.last_name = @last_name",
        parameters=[{"name": "@last_name", "value": last_name}],
        partition_key=school,
        enable_cross_partition_query=not same_partition,
    )

    # Assert
    assert items == actual


def test_update_non_existing_item(repository: StudentRepository):
    """Test update non existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student = create_test_student()

    with pytest.raises(CosmosResourceNotFoundError):
        repository.update(student)


def test_update_existing_item(repository: StudentRepository):
    """Test update existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student = create_test_student()

    repository.create_or_update(student)

    modified_student = create_test_student(
        student_id=student.id, school=student.school, last_name="Testing#Modified"
    )

    repository.update(modified_student)
    loaded = repository.get(student.id, student.school)

    # Assert
    assert loaded == modified_student


def test_create_new_item(repository: StudentRepository):
    """Test create new item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student = create_test_student()

    repository.create(student)

    loaded = repository.get(student.id, student.school)

    # Assert
    assert loaded == student


def test_create_existing_item(repository: StudentRepository):
    """Test create existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student = create_test_student()

    repository.create(student)

    # Assert
    with pytest.raises(CosmosResourceExistsError):
        repository.create(student)


def test_delete_existing_item(repository: StudentRepository):
    """Test delete existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    student = create_test_student()

    repository.create(student)

    loaded = repository.get(student.id, student.school)
    assert loaded == student

    repository.delete(student.id, student.school)
    assert repository.get(student.id, student.school) is None


def test_delete_non_existing_item(repository: StudentRepository):
    """Test delete existing item"""
    # Arrange
    if not repository:
        pytest.skip("Repository not configured for testing")

    # Act
    with pytest.raises(CosmosResourceNotFoundError):
        repository.delete(str(uuid.uuid4()), str(uuid.uuid4()))
