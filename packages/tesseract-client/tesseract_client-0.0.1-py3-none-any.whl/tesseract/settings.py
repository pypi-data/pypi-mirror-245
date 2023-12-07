from dataclasses import dataclass


@dataclass
class API_URL:
    base: str

    @property
    def signup(self) -> str:
        return self.base + '/auth/signup'

    @property
    def login(self) -> str:
        return self.base + '/auth/signin'

    @property
    def upload_file(self) -> str:
        return self.base + '/file'

    @property
    def delete_file(self) -> str:
        return self.base + '/file'

    @property
    def get_file_meta(self) -> str:
        return self.base + '/file'

    @property
    def upload_chunk(self) -> str:
        return self.base + '/chunk'

    @property
    def delete_chunk(self) -> str:
        return self.base + '/chunk'

    @property
    def get_chunk_meta(self) -> str:
        return self.base + '/chunk'

    @property
    def download_chunk(self) -> str:
        return self.base + '/chunk/download'


@dataclass
class Settings:
    username: str
    password: str
    folder: str
    db: str
    chunk_size: int
