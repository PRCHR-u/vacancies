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
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data has been written to {self._filename}")

    def read_from_file(self) -> list:
        """
        Reads data from a JSON file.
        """
        content = _read_file_content(self._filename)
        if content is not None:
            return json.loads(content)
        return []
