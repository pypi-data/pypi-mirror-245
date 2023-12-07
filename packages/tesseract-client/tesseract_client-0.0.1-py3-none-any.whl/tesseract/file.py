import os
import hashlib

from tesseract.chunk import Chunk, ChunkAction


class File:
    def __init__(
        self,
        file_path: str,
        root_folder: str = None,
        hash: str = None
    ):
        self.file_path = file_path
        self.root_folder = root_folder
        self.hash = hash or self.get_file_hash(
            self.get_absolute_path(self.file_path, self.root_folder)
        )

    def split_into_chunks(self, chunk_size: int) -> list[tuple[Chunk, bytes]]:
        """
        Returns a list of Chunk objects along with their data
        for the given file.
        """
        chunks = []
        path = self.get_absolute_path(self.file_path, self.root_folder)
        with open(path, 'rb') as file:
            chunk_num = 1
            while True:
                data = file.read(chunk_size)
                if not data:
                    break

                chunk_hash = hashlib.sha256(data).hexdigest()
                chunk = Chunk(
                    file_path=self.file_path,
                    order=chunk_num,
                    hash=chunk_hash
                )
                chunks.append((chunk, data))
                chunk_num += 1
        return chunks

    def get_updated_chunks(
        self,
        indexed_chunks: list[Chunk],
        chunk_size: int
    ) -> list[tuple[Chunk, bytes], ChunkAction]:
        """
        Returns a list of chunks that have been updated since the last time
        the file was indexed.
        """
        updated_chunks = []
        chunks = self.split_into_chunks(chunk_size)
        if len(chunks) > len(indexed_chunks):
            # File has been appended to
            for chunk in chunks[len(indexed_chunks):]:
                updated_chunks.append((chunk, ChunkAction.CREATE))
        elif len(chunks) < len(indexed_chunks):
            # File has been truncated
            for chunk in indexed_chunks[len(chunks):]:
                updated_chunks.append(((chunk, None), ChunkAction.DELETE))
        if len(indexed_chunks) > 0:
            for i, chunk in enumerate(chunks[:len(indexed_chunks)]):
                if chunk[0].hash != indexed_chunks[i].hash:
                    updated_chunks.append((chunk, ChunkAction.UPDATE))
        return updated_chunks

    @staticmethod
    def get_relative_path(file_path, root_folder) -> str:
        """Returns relative file path to the root folder."""
        return os.path.relpath(file_path, root_folder)

    @staticmethod
    def get_absolute_path(file_path, root_folder) -> str:
        """Returns the absolute path of the file."""
        return os.path.join(root_folder, file_path)

    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Returns the hash of a file."""
        with open(file_path, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()

    @classmethod
    def from_absolute_path(cls, file_path: str, root_folder: str):
        """Returns a File object from an absolute path."""
        return cls(
            root_folder=root_folder,
            file_path=os.path.relpath(file_path, root_folder)
        )
