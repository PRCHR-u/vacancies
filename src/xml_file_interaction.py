import xml.etree.ElementTree as ET
from src.abstract_file_interaction import FileInteraction
from src.utils import _read_file_content, _delete_file_content, _handle_file_error


class XMLSaver(FileInteraction):
    def __init__(self, filename: str = "vacancies.xml"):
        self._filename = filename

    def write_to_file(self, data: list) -> None:
        root = ET.Element("vacancies")
        for item in data:
            vacancy = ET.SubElement(root, "vacancy")
            for key, value in item.items():
                ET.SubElement(vacancy, key).text = str(value)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        try:
            tree.write(self._filename, encoding="utf-8", xml_declaration=True)
            print(f"Data has been written to {self._filename}")
        except Exception as e:
            print(f"An error occurred while writing to XML file: {e}")

    def read_from_file(self) -> list:
        file_content = _read_file_content(self._filename)
        if file_content is None:
            return []
        
        try:
            root = ET.fromstring(file_content)
        except ET.ParseError as e:
             _handle_file_error(self._filename, e, "parsing")
             return []
        data = []
        for vacancy_element in root.findall('vacancy'):
            vacancy_dict = {element.tag: element.text for element in vacancy_element}
            data.append(vacancy_dict)
        return data

    def delete_from_file(self) -> None:
         _delete_file_content(self._filename)