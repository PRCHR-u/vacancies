from src.abstract_file_interaction import FileInteraction
import csv
import os


class CSVSaver(FileInteraction):
    """
    A class for saving and reading data to/from a CSV file.
    """

    def __init__(self, filename: str = "vacancies.csv"):
        """
        Initializes CSVSaver with a filename.
        Args:
            filename: name of the csv file to save data to."""
        self._filename = filename

    def write_to_file(self, data: list[dict]):
        """Writes data to a CSV file."""
        with open(
            self._filename, "w", newline="", encoding="utf-8"
        ) as csvfile:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

    def read_from_file(self) -> list:
        """Reads data from a CSV file."""
        if not os.path.exists(self._filename):
            return []
        data = []
        with open(
            self._filename, "r", newline="", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def delete_from_file(self, filename: str = ""):
        """
        Deletes all data from the CSV file.
        """
        try:
            with open(self._filename, "w", encoding="utf-8"):
                ...
            print(f"Data in {self._filename} has been deleted.")
        except FileNotFoundError:
            print(f"File {self._filename} not found.")
        except Exception as e:
            print(f"An error occurred while deleting data: {e}")
