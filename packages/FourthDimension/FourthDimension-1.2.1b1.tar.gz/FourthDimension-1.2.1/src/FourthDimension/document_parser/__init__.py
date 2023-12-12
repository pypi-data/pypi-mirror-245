"""
文件说明：将各种类型的文件转成file类，然后转成document类
"""

__all__ = [
    "DocxParser",
    "JsonParser",
    "JsonlParser",
]

from FourthDimension.document_parser.docx_parser import DocxParser
from FourthDimension.document_parser.json_parser import JsonParser
from FourthDimension.document_parser.jsonl_parser import JsonlParser
