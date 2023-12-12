import io
import os

from fastapi import UploadFile

from FourthDimension.docstore.file import File
from FourthDimension.document_parser.base_parser import BaseParser

class JsonlParser(BaseParser):

    def parse(self, dir_path, file_name):
        """
        解析docx文件
        """
        with open(os.path.join(dir_path, file_name), "rb") as f:
            file_content = f.read()

        # Create a file-like object in memory using BytesIO
        file_object = io.BytesIO(file_content)
        upload_file = UploadFile(
            file=file_object, filename=file_name
        )
        file_instance = File(file=upload_file)
        file_instance.content = file_content

        # 处理docx文件（划分chunk和para并对齐）
        documents = self.process_docx(file_instance)
        return documents
