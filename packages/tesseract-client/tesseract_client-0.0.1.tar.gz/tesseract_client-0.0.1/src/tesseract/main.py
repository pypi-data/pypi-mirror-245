import os
import argparse

from watchdog.observers.polling import PollingObserver as Observer

from tesseract.settings import Settings, API_URL
from tesseract.db_manager import DBManager
from tesseract.services import Services
from tesseract.monitoring import FileChangeHandler
from tesseract.api_manager import APIManager


def create_folder_if_not_exists(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--username',
        '-u',
        help='Username to use for authentication',
        required=True
    )
    parser.add_argument(
        '--password',
        '-p',
        help='Password to use for authentication',
        required=True
    )
    parser.add_argument(
        '--folder',
        help='Folder to index',
        default='./test_folder'
    )
    parser.add_argument(
        '--db',
        help='Path to database file',
        default='chunk_hashes.db'
    )
    parser.add_argument(
        '--chunk-size',
        help='Chunk size in bytes',
        default=1000
    )
    parser.add_argument(
        '--api-url',
        help='URL of the API server',
        default='http://localhost:8000'
    )
    args = parser.parse_args()

    api_urls = API_URL(base=args.api_url)
    settings = Settings(
        username=args.username,
        password=args.password,
        folder=args.folder,
        db=args.db,
        chunk_size=args.chunk_size,
    )

    create_folder_if_not_exists(args.folder)

    with DBManager(args.db) as db_manager:
        api_manager = APIManager(
            username=args.username,
            password=args.password,
            api_urls=api_urls
        )
        services = Services(api_manager, db_manager, settings)
        event_handler = FileChangeHandler(services)

        # Check for changes that were made while offline
        services.check_for_offline_changes()

        # Pull updates from the server
        services.pull()

        # Start monitoring the folder for changes
        observer = Observer()
        observer.schedule(
            event_handler,
            path=args.folder,
            recursive=True
        )
        observer.start()
        print(f"Monitoring folder {args.folder} for updates...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()

        observer.join()


if __name__ == '__main__':
    main()
