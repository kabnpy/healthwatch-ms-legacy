import os
import shutil
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class StorageProvider(ABC):
    @abstractmethod
    def save_file(
        self, file: BinaryIO, filename: str, folder: str = "documents"
    ) -> str:
        """Saves a file and returns the relative path."""
        pass

    @abstractmethod
    def get_file_path(self, relative_path: str) -> Path:
        """Returns the absolute path for a given relative path."""
        pass

    @abstractmethod
    def delete_file(self, relative_path: str) -> bool:
        """Deletes a file from storage."""
        pass


class LocalFileSystemProvider(StorageProvider):
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = Path(base_dir)
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True)

    def save_file(
        self, file: BinaryIO, filename: str, folder: str = "documents"
    ) -> str:
        # Generate a unique filename to prevent collisions
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"

        # Create folder if it doesn't exist
        relative_folder = Path(folder)
        absolute_folder = self.base_dir / relative_folder
        if not absolute_folder.exists():
            absolute_folder.mkdir(parents=True)

        relative_path = relative_folder / unique_filename
        absolute_path = self.base_dir / relative_path

        with absolute_path.open("wb") as buffer:
            shutil.copyfileobj(file, buffer)

        return str(relative_path)

    def get_file_path(self, relative_path: str) -> Path:
        return self.base_dir / Path(relative_path)

    def delete_file(self, relative_path: str) -> bool:
        absolute_path = self.get_file_path(relative_path)
        if absolute_path.exists():
            absolute_path.unlink()
            return True
        return False


# Singleton instance
storage = LocalFileSystemProvider(base_dir=os.getenv("STORAGE_BASE_DIR", "storage"))
