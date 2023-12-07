import sqlite3
from tesseract.file import File, Chunk


class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.init_db()
        return self

    def __exit__(self, *_):
        self.db.close()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_path TEXT PRIMARY KEY,
                hash TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                file_path TEXT NOT NULL,
                order_num INTEGER NOT NULL,
                chunk_hash TEXT NOT NULL,
                PRIMARY KEY (file_path, order_num),
                FOREIGN KEY (file_path) REFERENCES files (file_path)
            )
        """)
        self.db.commit()

    def create_file(self, file: File):
        self.cursor.execute(
            "INSERT INTO files (file_path, hash) VALUES (?, ?)",
            (file.file_path, file.hash)
        )
        self.db.commit()

    def create_chunk(self, chunk: Chunk):
        self.cursor.execute(
            "INSERT INTO chunks (file_path, order_num, chunk_hash) VALUES (?, ?, ?)",
            (chunk.file_path, chunk.order, chunk.hash)
        )
        self.db.commit()

    def update_file(self, file: File):
        self.cursor.execute(
            "UPDATE files SET hash=? WHERE file_path=?",
            (file.hash, file.file_path)
        )
        self.db.commit()

    def update_chunk(self, chunk: Chunk):
        self.cursor.execute(
            "UPDATE chunks SET chunk_hash=? WHERE file_path=? AND order_num=?",
            (chunk.hash, chunk.file_path, chunk.order)
        )
        self.db.commit()

    def delete_file(self, file_path: str):
        self.cursor.execute("DELETE FROM files WHERE file_path=?", (file_path, ))
        self.cursor.execute("DELETE FROM chunks WHERE file_path=?", (file_path, ))
        self.db.commit()

    def delete_chunk(self, chunk: Chunk):
        self.cursor.execute(
            "DELETE FROM chunks WHERE file_path=? AND order_num=?",
            (chunk.file_path, chunk.order)
        )
        self.db.commit()

    def get_chunks(self, file_path: str):
        self.cursor.execute(
            "SELECT file_path, order_num, chunk_hash FROM chunks WHERE file_path=?",
            (file_path, )
        )
        return [
            Chunk(file_path=row[0], order=row[1], hash=row[2])
            for row in self.cursor.fetchall()
        ]

    def get_files(self):
        self.cursor.execute("SELECT file_path, hash FROM files")
        return [
            File(file_path=row[0], hash=row[1])
            for row in self.cursor.fetchall()
        ]

    def get_file_by_path(self, file_path: str):
        self.cursor.execute(
            "SELECT file_path, hash FROM files WHERE file_path=?", (file_path, )
        )
        row = self.cursor.fetchone()
        if row:
            return File(file_path=row[0], hash=row[1])
        else:
            return None
