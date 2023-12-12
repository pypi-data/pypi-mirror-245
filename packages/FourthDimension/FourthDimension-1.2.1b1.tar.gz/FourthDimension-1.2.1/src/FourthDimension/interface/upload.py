from FourthDimension.config import index_name
from FourthDimension.config.config import fds_client


def upload_entrance(all_documents):
    """
    存储入口
    :param all_documents: 段落列表
    :return:
    """
    print('解析完成，文档上传中...')
    response_data:dict = fds_client.insert_data(all_documents, index_name)
    if response_data.get("state_code") == 200:
        print("文档成功上传！")
    else:
        state_code =response_data.get("state_code")
        log_detail = response_data.get("log_detail")
        raise Exception(f"文档上传失败！错误码：{state_code}\n日志信息：{log_detail}")
    print('---------------------------------')
