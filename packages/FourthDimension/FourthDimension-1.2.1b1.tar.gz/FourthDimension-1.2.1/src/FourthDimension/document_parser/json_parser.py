import io
import os

from fastapi import UploadFile

from FourthDimension.docstore.file import File
from FourthDimension.document_parser.base_parser import BaseParser


class JsonParser(BaseParser):

    def parse(self, dir_path, file_name):
        """
        解析docx文件 FIXME
        """
        return None