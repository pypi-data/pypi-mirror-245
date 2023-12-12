import os

from FourthDimension.document_parser import DocxParser, JsonlParser


def parse_data(doc_or_dir_path):
    """
    数据解析
    :param doc_or_dir_path: 文件路径或文件夹路径
    :return: list[FDDocument]
    """
    print('开始文档解析...')
    if os.path.isfile(doc_or_dir_path):  # 如果是文件
        fd_docs = get_fd_docs_from_file(doc_or_dir_path)
    elif os.path.isdir(doc_or_dir_path):  # 如果是目录
        fd_docs = get_fd_docs_from_dir(doc_or_dir_path)
    else:
        print(f"{doc_or_dir_path} 不是有效的文件或目录")
        exit(0)
    print('文档解析结束...')
    return fd_docs


def get_fd_docs_from_file(dir_path, file_name):
    fd_docs = None
    file_type = os.path.splitext(file_name)[1]
    # '/home/example.2.1.txt' -> '.txt'
    # 根据不同的file_type选择不同解析方式
    if 'docx' in file_type:
        parser = DocxParser()
        fd_docs = parser.parse(dir_path, file_name)
    elif 'jsonl' in file_type:
        parser = JsonlParser()
        fd_docs = parser.parse(dir_path, file_name)
    else:
        print(f"暂时不支持解析该类文件:{file_type}")
    return fd_docs


def get_fd_docs_from_dir(dir_path):
    # 遍历目录中的文件
    fd_docs = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):  # 如果是文件
            fd_docs.extend(get_fd_docs_from_file(dir_path, file_name))
    return fd_docs
