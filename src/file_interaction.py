import json
from src.abstract_file_interaction import FileInteraction
from src.utils import _read_file_content, _delete_file_content


class JSONSaver(FileInteraction):
    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename

    def delete_from_file(self) -> None:
        _delete_file_content(self._filename)

    def write_to_file(self, data: list) -> None:
        """
        Writes data to a JSON file.

        Args:
            data: A list of dictionaries to be written to the file.
        """
        existing_data = self.read_from_file()
        unique_data = existing_data[:]  # Start with existing data

        for item in data:
            if item not in unique_data:
                unique_data.append(item)

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(unique_data, file, indent=4, ensure_ascii=False)
        print(f"Data has been written to {self._filename}")

    def read_from_file(self) -> list:
        """
        Reads data from a JSON file.

        Returns:
            A list of dictionaries read from the file.
        """
        content = _read_file_content(self._filename)
        if content:
            return json.loads(content)
        return []
