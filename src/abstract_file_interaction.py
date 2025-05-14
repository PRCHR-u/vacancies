from abc import ABC, abstractmethod
from typing import List


class FileInteraction(ABC):
    """
    Abstract base class for file interaction.
    Defines the interface for writing to and reading from a file.
    """

    @abstractmethod
    def write_to_file(self, data: List[dict], filename: str) -> None:
        """
        Writes data to a file.

        Args:
            data: The data to write.
            filename: The name of the file to write to.
        """
        pass

    @abstractmethod
    def read_from_file(self, filename: str) -> List[dict]:
        """
        Reads data from a file.
        Args:
            filename: The name of the file to read from.
        """
        pass
