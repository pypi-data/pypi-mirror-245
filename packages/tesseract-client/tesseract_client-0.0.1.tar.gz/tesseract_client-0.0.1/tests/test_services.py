import os
import hashlib
import tempfile
import pytest

from unittest.mock import Mock
from app.config import settings
from app.api_manager import APIManager
from app.db_manager import DBManager
from app.services import Services


def create_temp_file(file_name: str, content: str) -> str:
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file_name)
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(content)
    return temp_file_path


@pytest.fixture
def services() -> Services:
    """Creates a temporary database and returns a Services instance."""
    db_fd, settings.db_path = tempfile.mkstemp()
    with DBManager(settings.db_path) as db:
        api_manager = Mock(spec=APIManager)
        yield Services(api_manager, db)
    os.close(db_fd)
    os.unlink(settings.db_path)


def test_get_file_hash():
    file_path = create_temp_file("test.txt", "test content")
    hash = Services.get_file_hash(file_path)
    assert hash == hashlib.sha256("test content".encode()).hexdigest()


# def test_split_into_chunks():
#     file_path = create_temp_file("test.txt", "test content")
#     chunks = Services.split_into_chunks(file_path, chunk_size=1024)
#     assert len(chunks) == 1
#     assert chunks[0].order == 1
#     assert chunks[0].hash == hashlib.sha256(
#       "test content".encode()
#     ).hexdigest()


# def test_create_file(services: Services):
#     file_path = create_temp_file("test.txt", "test content")
#     services.create_file(file_path)

#     # Retrieve the file from the database and assert its attributes
#     print(services.db_manager.get_files())
#     retrieved_file = services.db_manager.get_file_by_path("test.txt")
#     print(retrieved_file)
#     assert retrieved_file.file_path == "test.txt"
#     assert retrieved_file.hash == hashlib.md5(
#         "test content".encode()
#     ).hexdigest()
