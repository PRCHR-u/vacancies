from abc import ABC, abstractmethod

class FileInteraction(ABC):
    @abstractmethod
    def write_to_file(self, data, filename):
        pass

    @abstractmethod
    def read_from_file(self, filename):
        pass