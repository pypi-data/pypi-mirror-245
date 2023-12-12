import jpype
import os
from typing import List, Dict
import json

from FourthDimension.config import resource_dir
from FourthDimension.docstore.document import FDDocument


class FdsClient:
    """
     FdSearch 客户端，提供Python调用Java对应的函数。

     .. 代码块:: python
         fds_client = FdsClient()

         # 插入文档API
        fds_client.insert_data(all_documents, index_name)

         # QA文档检索API

         # QA向量检索API
    """
    def __init__(self) -> None:
        # getDefaultJVMPath 获取默认的 JVM 路径
        # jvm_path = jpype.getDefaultJVMPath()
        jvm_path = os.path.join(resource_dir, 'jdk', 'lib', 'server', 'libjvm.so')
        jpype.startJVM(jvm_path, '-ea', convertStrings=False)
        fds_path = os.path.join(resource_dir, "FourthDimension-search.jar")
        jpype.addClassPath(fds_path)

        self.JavaFDDocument = jpype.JClass('cn.yantu.fourthdimension.index.mapper.FDDocument')
        self.JavaArrayList = jpype.JClass('java.util.ArrayList')
        self.JavaMain = jpype.JClass('cn.yantu.fourthdimension.Main')
        self.main = self.JavaMain()

    def create_index(self):
        raise Exception("Unimplemented")

    def insert_data(self, all_documents: List[FDDocument], index_name: str) -> dict:
        javaDocumentList = self.JavaArrayList()
        for doc in all_documents:
            javaFDDocument = self.JavaFDDocument()
            javaFDDocument.setChunk_context(doc.chunk_context)
            javaFDDocument.setFile_name(doc.file_name)
            javaFDDocument.setPara_num(doc.para_num)
            javaFDDocument.setChunk_vector(doc.chunk_vector)
            javaFDDocument.setPara_contexts(self.JavaArrayList(doc.para_contexts))
            javaDocumentList.add(javaFDDocument)
        response = self.main.insertDocuments(javaDocumentList, index_name)
        response_json = json.loads(str(response))
        return {
            'state_code': response_json['code'],
            'log_detail': response_json['message']
        }

    def search_filename(self):
        raise Exception("Unimplemented")

    def clean_data(self, index_name: str):
        response = self.main.cleanDocuments(index_name)
        response_json = json.loads(str(response))
        return {
            'state_code': response_json['code'],
            'log_detail': response_json['message']
        }

    def es_search_para(self, para_num, file_name):
        raise Exception("Unimplemented")

    def fds_search(self, question: str, anal_question: str, index_name: str) -> Dict:
        response = self.main.searchDocuments(question, anal_question, index_name)
        response_json = json.loads(str(response))
        response_documents = response_json['data']
        contexts = []
        for doc in response_documents:
            contexts.append(FDDocument(
                file_name=doc['file_name'],
                chunk_context=doc['chunk_context'],
                para_num=doc['para_num'],
                para_contexts=doc['para_contexts']
            ))
        return {
            'state_code': response_json['code'],
            'log_detail': response_json['message'],
            'contexts': contexts
        }

    def fds_search_vectors(self, query_vector: List[float], index_name: str) -> Dict:
        response = self.main.searchVectors(query_vector, index_name)
        response_json = json.loads(str(response))
        response_documents = response_json['data']
        contexts = []
        for doc in response_documents:
            contexts.append(FDDocument(
                file_name=doc['file_name'],
                chunk_context=doc['chunk_context'],
                para_num=doc['para_num'],
                para_contexts=doc['para_contexts']
            ))
        return {
            'state_code': response_json['code'],
            'log_detail': response_json['message'],
            'contexts': contexts
        }

    def shutdown(self):
        # shutdownJVM()关闭JAVA虚拟机
        jpype.shutdownJVM()


if __name__ == "__main__":
    import json
