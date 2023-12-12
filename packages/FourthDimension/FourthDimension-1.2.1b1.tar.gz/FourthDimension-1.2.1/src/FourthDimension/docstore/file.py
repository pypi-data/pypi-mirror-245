import json
import os
import tempfile
from typing import Any, Optional
from uuid import UUID

from fastapi import UploadFile

from FourthDimension.chain.document import Document
from FourthDimension.chain.text_splitter import RecursiveCharacterTextSplitter
from FourthDimension.chain.pydantic import BaseModel

from FourthDimension.docstore.document import FDDocument
from FourthDimension.config import (
    config_setting,
    chunk_overlap,
    max_para_len,
    max_chunk_len,
    min_single_para_len
)
from FourthDimension.util.fd_util import (get_tokens_from_string, compute_sha1_from_file)

chunk_size = config_setting['para_config']['chunk_size']
# chunk_overlap = config_setting['para_config']['overlap']



class File(BaseModel):
    id: Optional[UUID] = None
    file: Optional[UploadFile]
    file_name: Optional[str] = ""
    file_size: Optional[int] = None
    file_sha1: Optional[str] = ""
    vectors_ids: Optional[list] = []
    file_extension: Optional[str] = ""
    content: Optional[Any] = None
    chunk_size: int = chunk_size
    chunk_overlap: int = chunk_overlap
    origin_documents: Optional[Any] = None
    para_documents: Optional[Any] = None
    chunk_documents: Optional[Any] = None

    fd_documents: Optional[Any] = None
    chunk_text_splitter: Optional[Any] = None
    para_text_splitter: Optional[Any] = None
    min_single_para_len: int = min_single_para_len
    max_para_len: int = max_para_len

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.file:
            self.para_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=max_para_len, chunk_overlap=chunk_overlap)
            self.chunk_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=max_chunk_len, chunk_overlap=chunk_overlap)
            self.file_name = self.file.filename
            self.file_size = None  # pyright: ignore reportPrivateUsage=none
            self.file_extension = os.path.splitext(
                self.file.filename  # pyright: ignore reportPrivateUsage=none
            )[-1].lower()

    async def compute_file_sha1(self):
        """
        Compute the sha1 of the file using a temporary file
        """
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            await self.file.seek(0)  # pyright: ignore reportPrivateUsage=none
            self.content = (
                await self.file.read()  # pyright: ignore reportPrivateUsage=none
            )
            tmp_file.write(self.content)
            tmp_file.flush()
            self.file_sha1 = compute_sha1_from_file(tmp_file.name)

        os.remove(tmp_file.name)

    def compute_para(self, documents):
        content = documents[0].page_content
        file_name = documents[0].metadata['source']
        all_para = []
        split_content = content.split('\n')
        current_para = split_content[0]
        for i in range(1, len(split_content)):
            line = split_content[i]
            current_para_len = get_tokens_from_string(current_para)
            line_len = get_tokens_from_string(line)
            # 若单段长度小于总段限长
            if line_len < max_para_len:
                # 若本段加上下一段的长度小于总段限长，则两段拼接
                if current_para_len + line_len < max_para_len:
                    if current_para != "":
                        current_para += '\n' + line
                    else:
                        current_para += line
                    if line_len >= min_single_para_len:
                        all_para.append(current_para)
                        current_para = ""
                else:
                    # 若本段加上下一段的长度大于总段限长，则归类为一个自然段
                    all_para.append(current_para)
                    current_para = line
            else:
                # 切分过长段落
                # if current_para != "" and current_para not in all_para:
                if current_para != "":
                    all_para.append(current_para)
                line_para_documents = [Document(page_content=line, metadata={'source': file_name})]
                line_para_documents = self.para_text_splitter.split_documents(line_para_documents)
                current_para = line_para_documents[0].page_content
                for j in range(1, len(line_para_documents)):
                    # 切分后的段落
                    current_para_len = get_tokens_from_string(current_para)
                    current_line = line_para_documents[j].page_content
                    current_line_len = get_tokens_from_string(current_line)

                    if current_para_len + current_line_len < max_para_len:
                        if current_para != "":
                            # current_para += current_line
                            current_para += '\n' + current_line
                        else:
                            current_para += current_line
                        if current_line_len >= min_single_para_len:
                            all_para.append(current_para)
                            current_para = ""
                    else:
                        # 若本段加上下一段的长度大于总段限长，则归类为一个自然段
                        all_para.append(current_para)
                        current_para = current_line
        # 处理最后一个自然段
        if current_para != "":
            all_para.append(current_para)
        # with open('德国喜宝HIPP纯天然有机婴儿奶粉_para.json', 'w', encoding='utf-8') as fr:
        #     json.dump(all_para, fr, indent=4, ensure_ascii=False)
        # 封装document
        # all_para_document = []
        all_fd_document = []
        for i, para in enumerate(all_para):
            all_fd_document.append(FDDocument(para_num=i,
                                              file_name=file_name,
                                              chunk_context=para
                                              ))
            # all_para_document.append(Document(page_content=para, metadata={'source': file_name,
            #                                                                'para_num': i,
            #                                                                'type': 'para'}))
        # 存储Document对应的内容
        # self.save_all_para_documents(all_para,file_name)
        # return all_para_document
        return all_fd_document

    def save_all_para_documents(self, all_para, file_name):
        all_para_contexts = [{"para_num": i, "file_name": file_name, "para": para} for i, para in enumerate(all_para)]
        with open("all_para_documents.json", "w", encoding='utf-8') as fw:
            json.dump(all_para_contexts, fw, ensure_ascii=False, indent=4)
        pass

    def compute_documents(self, loader_class):
        """
        Compute the documents from the file

        Args:
            loader_class (class): The class of the loader to use to load the file
        """
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            tmp_file.write(self.content)  # pyright: ignore reportPrivateUsage=none
            tmp_file.flush()
            loader = loader_class(tmp_file.name)
            documents = loader.load()

        os.remove(tmp_file.name)
        self.origin_documents = documents
        self.para_documents = self.compute_para(documents)
        self.chunk_documents = self.parse_chunk_documents(documents)
        self.mapping_chunk2para()

    def mapping_chunk2para(self):
        origin_docx_text = self.origin_documents[0].page_content
        para_index_in_chunk = []
        chunk_index_in_origin_docx = []
        para_index_in_origin_docx = []
        #  chunk_documents定位
        for i, chunk_doc in enumerate(self.chunk_documents):
            chunk_doc: FDDocument
            chunk_context = chunk_doc.get_chunk_context()
            start = origin_docx_text.find(chunk_context)
            end = start + len(chunk_context) - 1
            chunk_index_in_origin_docx.append(
                (chunk_context, start, end)
            )
        #  para_documents定位
        for i, para_doc in enumerate(self.para_documents):
            para_doc: FDDocument
            para_context = para_doc.get_chunk_context()
            start = origin_docx_text.find(para_context)
            end = start + len(para_context) - 1

            para_index_in_origin_docx.append(
                (para_context, start, end)
            )

        current_start = -1
        current_end = -1
        for i, chunk_index in enumerate(chunk_index_in_origin_docx):
            chunk_st = chunk_index[1]
            chunk_end = chunk_index[2]
            contain_st_idx = -1
            contain_end_idx = -1
            for j, para_index in enumerate(para_index_in_origin_docx):
                para_st = para_index[1]
                para_end = para_index[2]
                if para_st <= chunk_st <= para_end and contain_st_idx == -1:
                    contain_st_idx = j
                if para_st <= chunk_end <= para_end and contain_end_idx == -1:
                    contain_end_idx = j
            if contain_st_idx != -1:
                if contain_end_idx != -1:
                    current_start = contain_st_idx
                    current_end = contain_end_idx + 1
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx, contain_end_idx + 1)]
                    )
                else:
                    contain_end_idx = contain_st_idx
                    current_start = contain_st_idx
                    current_end = contain_end_idx + 1
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx, contain_end_idx + 1)]
                    )
            else:
                if contain_end_idx != -1:
                    contain_st_idx = contain_end_idx
                    current_start = contain_st_idx - 1
                    current_end = contain_end_idx
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx - 1, contain_end_idx)]
                    )
                else:
                    # print(chunk_index)
                    contain_st_idx = current_start
                    contain_end_idx = current_end
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx, contain_end_idx)]
                    )

        for i in range(len(self.chunk_documents)):
            # self.chunk_documents[i].metadata['para_num'] = list(para_index_in_chunk[i])
            self.chunk_documents[i].set_para_num(list(para_index_in_chunk[i]))
            self.chunk_documents[i].set_para_contexts([self.para_documents[i_].get_chunk_context()
                                                       for i_ in para_index_in_chunk[i]
                                                       ])

    def parse_chunk_documents(self, documents):
        chunk_documents = self.chunk_text_splitter.split_documents(documents)
        chunk_fd_documents = []
        for chunk_document in chunk_documents:
            chunk_fd_documents.append(FDDocument(chunk_context=chunk_document.page_content))
        return chunk_fd_documents
