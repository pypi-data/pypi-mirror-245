import os
import hashlib

from tesseract.settings import Settings
from tesseract.api_manager import APIManager
from tesseract.db_manager import DBManager
from tesseract.file import File, Chunk, ChunkAction


class Services:
    """Provides business logic for the application."""
    def __init__(
        self,
        api_manager: APIManager,
        db_manager: DBManager,
        settings: Settings
    ):
        self.api_manager = api_manager
        self.db_manager = db_manager
        self.settings = settings

    def create_file(self, file_path: str):
        """Creates a new file in the database and uploads it to the server."""
        file = File.from_absolute_path(file_path, self.settings.folder)
        self.db_manager.create_file(file)
        # self.api_manager.upload_file(file)
        for chunk, data in file.split_into_chunks(self.settings.chunk_size):
            self.create_chunk(chunk, data)

    def update_file(self, file_path: str):
        """
        Updates an existing file in the database and uploads it to the server.
        """
        file = File.from_absolute_path(file_path, self.settings.folder)
        indexed_file = self.db_manager.get_file_by_path(
            file.file_path
        )
        # Check if the file was actually modified
        if indexed_file.hash == file.hash:
            return
        self.db_manager.update_file(file)
        # self.api_manager.upload_file(file)
        indexed_chunks = self.db_manager.get_chunks(file.file_path)
        updated_chunks = file.get_updated_chunks(
            indexed_chunks,
            self.settings.chunk_size
        )
        print(updated_chunks)
        for (chunk, data), action in updated_chunks:
            if action == ChunkAction.CREATE:
                self.create_chunk(chunk, data)
            elif action == ChunkAction.DELETE:
                self.delete_chunk(chunk)
            else:
                self.update_chunk(chunk, data)

    def delete_file(self, file_path: str):
        """Deletes a file from the database and the server."""
        self.db_manager.delete_file(
            File.get_relative_path(file_path, self.settings.folder)
        )
        # self.api_manager.delete_file(file_path)

    def create_chunk(self, chunk: Chunk, data: bytes):
        """Creates a new chunk in the database and uploads it to the server."""
        self.db_manager.create_chunk(chunk)
        # self.api_manager.upload_chunk(chunk, data)

    def update_chunk(self, chunk: Chunk, data: bytes):
        """
        Updates an existing chunk in the database and uploads it to the server.
        """
        self.db_manager.update_chunk(chunk)
        # self.api_manager.upload_chunk(chunk, data)

    def delete_chunk(self, chunk: Chunk):
        """Deletes a chunk from the database and the server."""
        self.db_manager.delete_chunk(chunk)
        # self.api_manager.delete_chunk(chunk)

    def check_for_offline_changes(self):
        """Checks for changes that were made while offline."""
        self._check_for_offline_deletions()
        self._check_for_offline_updates(self.settings.folder)

    def _check_for_offline_deletions(self):
        """Checks for files that were deleted while offline."""
        folder = self.settings.folder
        db_files = self.db_manager.get_files()
        local_files = []
        for root, _, files in os.walk(folder):
            for file in files:
                # file = os.path.join(root, file)
                file = File.get_relative_path(file, folder)
                local_files.append(file)
        for db_file in db_files:
            if db_file.file_path not in local_files:
                self.delete_file(File.get_absolute_path(
                    db_file.file_path,
                    folder
                ))

    def _check_for_offline_updates(self, folder: str = None):
        """Checks for files that were created/modified while offline."""
        for file in os.listdir(folder):
            file = os.path.join(folder, file)
            if os.path.isdir(file):
                self._check_for_offline_updates(file)
            else:
                db_file = self.db_manager.get_file_by_path(
                    File.get_relative_path(file, self.settings.folder)
                )
                if db_file:
                    if db_file.hash != File.get_file_hash(file):
                        self.update_file(file)
                else:
                    self.create_file(file)

    def pull(self):
        # TODO
        """Pulls the latest changes from the server."""
        pass
