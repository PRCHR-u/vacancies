import os
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import mock_open, patch
import json
import csv
import xml.etree.ElementTree as ET

from src.file_interaction import JSONSaver
from src.xml_file_interaction import XMLSaver
from src.csv_file_interaction import CSVSaver

class TestJSONSaver:
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_write_to_file(self, mock_json_dump, mock_file):
        saver = JSONSaver(filename="test.json")
        data = [{"key": "value"}]
        saver.write_to_file(data)

        mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(data, mock_file.return_value, indent=4, ensure_ascii=False)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"key": "value"}]')
    def test_read_from_file(self, mock_file):
        saver = JSONSaver(filename="test.json")
        result = saver.read_from_file()

        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")
        assert result == [{"key": "value"}]

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_read_from_file_file_not_found(self, mock_json_load, mock_file):
        mock_file.side_effect = FileNotFoundError
        saver = JSONSaver(filename="test.json")

        result = saver.read_from_file()
        assert result == []

class TestXMLSaver:
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(ET.ElementTree, 'write')
    def test_write_to_file(self, mock_tree_write, mock_file):
        saver = XMLSaver(filename="test.xml")

        data = [{"key": "value"}]
        saver.write_to_file(data)

        mock_file.assert_called_once_with("test.xml", 'w', encoding='utf-8')
        mock_tree_write.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='<vacancies><vacancy><key>value</key></vacancy></vacancies>')
    @patch.object(ET, 'parse')
    def test_read_from_file(self, mock_parse, mock_file):
        mock_parse.return_value.getroot.return_value.findall.return_value = [
            ET.fromstring('<vacancy><key>value</key></vacancy>')
        ]

        saver = XMLSaver(filename="test.xml")
        result = saver.read_from_file()

        mock_file.assert_called_once_with("test.xml", 'r', encoding='utf-8')
        assert result == [{'key': 'value'}]
    
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(ET, 'parse')
    def test_read_from_file_file_not_found(self, mock_parse, mock_file):

        mock_parse.side_effect = FileNotFoundError

        saver = XMLSaver(filename="test.xml")
        result = saver.read_from_file()

        assert result == []

class TestCSVSaver:
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(csv.DictWriter, 'writeheader')
    @patch.object(csv.DictWriter, 'writerows')
    def test_write_to_file(self, mock_writerows, mock_writeheader, mock_file):
        saver = CSVSaver(filename="test.csv")

        data = [{"key": "value"}]
        saver.write_to_file(data)

        mock_file.assert_called_once_with("test.csv", 'w', newline='', encoding='utf-8')
        mock_writeheader.assert_called_once()
        mock_writerows.assert_called_once_with(data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.DictReader")
    @patch('os.path.exists', return_value=True)
    def test_read_from_file(self, mock_path_exists, mock_csv_reader, mock_file):

        mock_csv_reader.return_value = [{'key': 'value'}]

        saver = CSVSaver(filename="test.csv")
        result = saver.read_from_file()

        mock_file.assert_called_once_with("test.csv", 'r', newline='', encoding='utf-8')
        assert result == [{'key': 'value'}]

    @patch('os.path.exists', return_value=False)
    def test_read_from_file_file_not_found(self, mock_path_exists):
        saver = CSVSaver(filename="test.csv")

        result = saver.read_from_file()
        assert result == []