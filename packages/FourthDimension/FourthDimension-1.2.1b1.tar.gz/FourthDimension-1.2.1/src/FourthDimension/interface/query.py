from typing import List

from FourthDimension.config import search_select, index_name
from FourthDimension.config.config import fds_client
from FourthDimension.docstore.document import FDDocument
from FourthDimension.util.fd_util import question_analysis, get_embedding, text_vector_rerank


def query_entrance(question) -> List[FDDocument]:
    """
    查询入口
    :param question: 问题
    :return:
    """
    print('开始检索问题：{}'.format(question))
    if search_select == "default":
        # 向量查询和文本查询的并集
        top_k_fd_documents = lucene_query(question)
    else:
        raise Exception(f"参数search_select无法匹配，请检查参数：f{search_select}")
        # print(f"参数search_select无法匹配，请检查参数：f{search_select}")
    # 重排fd_documents
    processed_fd_document_context = postprocess_fd_documents(question, top_k_fd_documents)
    return processed_fd_document_context


def lucene_query(question: str) -> List[FDDocument]:
    """
    lucene 查询文本和查询向量
    :param question: 问题
    """
    # 文本查询
    question_anal = question_analysis(question=question)
    text_search_fd_documents_response = fds_client.fds_search(question=question,
                                                     anal_question=question_anal,
                                                     index_name=index_name)
    text_search_fd_documents = ""
    if text_search_fd_documents_response.get('state_code') != 200:
        lucene_log_detail = text_search_fd_documents_response.get('log_detail',"not known")
        lucene_status_code= text_search_fd_documents_response.get('status_code',"not known")
        raise Exception(f"Lucene文本查询失败！错误码：{lucene_status_code}\n日志信息：{lucene_log_detail}")
    else:
        text_search_fd_documents= text_search_fd_documents_response.get("contexts")

    # 向量查询
    embedded_query = get_embedding(question)
    vector_search_fd_documents_response = fds_client.fds_search_vectors(query_vector=embedded_query, index_name=index_name)
    if vector_search_fd_documents_response.get("state_code") != 200:
        lucene_log_detail = vector_search_fd_documents_response.get('log_detail',"not known")
        lucene_status_code = vector_search_fd_documents_response.get('status_code','not known')
        raise Exception(f"Lucene向量查询失败！错误码：{lucene_status_code}\n日志信息：{lucene_log_detail}")
    else:
        vector_search_fd_documents= vector_search_fd_documents_response.get("contexts")
    # fds_client

    # 合并查询结果
    # Merge text_search_fd_documents + vector_search_fd_documents
    return list(set(vector_search_fd_documents + text_search_fd_documents))


def postprocess_fd_documents(question: str, top_k_fd_documents: List[FDDocument]) -> List[FDDocument]:
    # FIXME 重排
    reranked_top_k_fd_documents = text_vector_rerank(question=question, fd_documents = top_k_fd_documents)
    reranked_top_k_fd_documents_context = ["".join(fd_document.get_para_contexts()) for fd_document in reranked_top_k_fd_documents]
    return reranked_top_k_fd_documents_context

