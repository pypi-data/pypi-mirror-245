from FourthDimension.chain.loader import Docx2txtLoader
from FourthDimension.docstore.common import process_file
from FourthDimension.docstore.file import File
from FourthDimension.util.fd_util import replace_multiple_newlines, get_embedding


class BaseParser():
    def process_docx(self, file: File):
        """
        处理chunk并对齐
        """
        documents = []

        file = process_file(
            file=file,
            loader_class=Docx2txtLoader
        )
        file_name = file.file_name
        documents.extend(file.chunk_documents)
        # documents.extend(file.para_documents)
        for i, d in enumerate(documents):
            # 更新chunk_context: 去除多个换行符
            # 更新chunk_vector
            # 更新文件名
            # documents[i].page_content = replace_multiple_newlines(documents[i].page_content)
            filtered_chunk_context = replace_multiple_newlines(documents[i].get_chunk_context())
            chunk_vector = get_embedding(filtered_chunk_context)
            documents[i].set_chunk_vector(chunk_vector)
            documents[i].set_chunk_context(filtered_chunk_context)
            # documents[i].metadata['source'] = os.path.basename(documents[i].metadata['source'])
            documents[i].set_file_name(file_name)
        return documents

    def parse(self, dir_path, file_name):
        pass
