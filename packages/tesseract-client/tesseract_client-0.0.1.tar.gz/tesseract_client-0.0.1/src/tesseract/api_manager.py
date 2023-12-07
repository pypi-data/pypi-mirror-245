import functools
import requests

from tesseract.settings import API_URL
from tesseract.file import Chunk, File


class InvalidCredentials(Exception):
    pass


class APIManager:
    """Handles communication with the server."""
    def __init__(self, username: str, password: str, api_urls: API_URL):
        self.access_token = None
        self.username = username
        self.password = password
        self.api_urls = api_urls

    def login(self):
        """Logs in to the server and stores the access token."""
        response = requests.post(
            self.api_urls.login,
            data={"username": self.username, "password": self.password}
        )
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
        else:
            raise InvalidCredentials("Invalid username or password")

    def renew_token(func):
        """Decorator that renews the access token if it has expired."""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except InvalidCredentials:
                self.login()
                return func(self, *args, **kwargs)
        return wrapper

    @renew_token
    def _make_request(
        self,
        method: callable,
        url: str,
        status_code: int,
        **kwargs
    ) -> requests.Response:
        """Makes a request to the server."""
        response = method(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            **kwargs
        )
        if response.status_code == status_code:
            return response
        if response.status_code == 401:
            raise InvalidCredentials("Invalid access token")
        else:
            raise Exception(response.json()['detail'])

    def upload_file(self, file: File):
        """Uploads a file to the server"""
        self._make_request(
            requests.post,
            self.api_urls.upload_file,
            status_code=201,
            json={"file_name": file.file_path, "hash": file.hash}
        )

    def delete_file(self, file: File):
        """Deletes a file from the server"""
        self._make_request(
            requests.delete,
            self.api_urls.delete_file,
            status_code=204,
            json={"file_path": file.file_path}
        )

    def get_file_meta(self, file_path: str):
        """Gets the metadata of a file from the server"""
        return self._make_request(
            requests.get,
            self.api_urls.get_file_meta,
            status_code=200,
            json={"file_path": file_path}
        )

    def upload_chunk(self, chunk: Chunk, data: bytes):
        """Uploads a chunk to the server"""
        self._make_request(
            requests.post,
            self.api_urls.upload_chunk,
            status_code=201,
            json={
                "file_path": chunk.file_path,
                "order_num": chunk.order,
                "hash": chunk.hash
            },
            data=data
        )

    def delete_chunk(self, file_path: str, order: int):
        """Deletes a chunk from the server"""
        self._make_request(
            requests.delete,
            self.api_urls.delete_chunk,
            status_code=204,
            json={
                "file_path": file_path,
                "order_num": order
            }
        )

    def get_chunk_meta(self, file_path: str, order: int):
        """Gets the metadata of a chunk from the server"""
        return self._make_request(
            requests.get,
            self.api_urls.get_chunk_meta,
            status_code=200,
            json={
                "file_path": file_path,
                "order_num": order
            }
        )

    def download_chunk(self, file_path: str, order: int):
        """Downloads a chunk from the server"""
        return self._make_request(
            requests.get,
            self.api_urls.download_chunk,
            status_code=200,
            json={
                "file_path": file_path,
                "order_num": order
            }
        ).content
