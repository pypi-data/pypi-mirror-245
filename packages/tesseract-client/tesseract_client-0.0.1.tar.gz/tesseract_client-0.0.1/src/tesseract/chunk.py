from dataclasses import dataclass
from enum import Enum


@dataclass
class Chunk:
    file_path: str
    order: int
    hash: str


class ChunkAction(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
