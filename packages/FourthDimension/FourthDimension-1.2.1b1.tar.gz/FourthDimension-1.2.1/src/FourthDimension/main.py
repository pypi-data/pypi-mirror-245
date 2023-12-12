import time

from FourthDimension.model import chatGPT

from FourthDimension.interface.clean import clean_entrance
from FourthDimension.interface.parse import parse_data
from FourthDimension.interface.query import query_entrance
from FourthDimension.interface.upload import upload_entrance


def upload(doc_or_dir_path):
    """
    文档上传接口
    数据格式List[Document]
    :param doc_or_dir_path:
    :return:
    """
    all_documents = parse_data(doc_or_dir_path)
    upload_entrance(all_documents)


def query(question):
    """
    检索增强生成(问答)接口
    :param question: 问题
    :return:
    """
    top_k_contexts = query_entrance(question)
    # print(f"提供的上下文是：{top_k_contexts}")
    answer = chatGPT.answer_generate(question, top_k_contexts)
    # print(f"答案是：\n{answer}")
    return answer


def clean():
    """
    清除所有数据
    """
    clean_entrance()


if __name__ == "__main__":
    # upload("../../data")
    start_time = time.time()
    query("毕业论文的格式是什么？")
    print(f"cost time:{time.time()-start_time}")