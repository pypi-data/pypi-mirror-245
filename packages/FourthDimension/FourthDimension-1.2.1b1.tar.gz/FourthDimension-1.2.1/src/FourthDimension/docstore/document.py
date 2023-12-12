from typing import List


class FDDocument:
    # lucene存储基本单元 fd_document
    def __init__(self,
                 file_name: str = None,
                 chunk_context: str = None,
                 chunk_vector: List[float] = None,
                 para_num: List[int] = None,
                 para_contexts: List[str] = None,
                 ):
        self.file_name = file_name
        self.chunk_context = chunk_context
        self.chunk_vector = chunk_vector
        self.para_num = para_num
        self.para_contexts = para_contexts

    # 生成get方法
    def get_file_name(self):
        return self.file_name

    def get_chunk_context(self):
        return self.chunk_context

    def get_chunk_vector(self):
        return self.chunk_vector

    def get_para_num(self):
        return self.para_num

    def get_para_contexts(self):
        return self.para_contexts

    # 生成set方法
    def set_file_name(self, file_name):
        self.file_name = file_name

    def set_chunk_context(self, chunk_context):
        self.chunk_context = chunk_context

    def set_chunk_vector(self, chunk_vector):
        self.chunk_vector = chunk_vector

    def set_para_num(self, para_num):
        self.para_num = para_num

    def set_para_contexts(self, para_contexts):
        self.para_contexts = para_contexts
