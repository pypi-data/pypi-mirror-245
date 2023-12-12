from FourthDimension.config import index_name
from FourthDimension.config.config import fds_client

def clean_entrance():
    print('正在清空文档...')
    response_data: dict = fds_client.clean_data(index_name)
    if response_data.get("state_code") == 200:
        print("文档清空成功！")
    else:
        state_code =response_data.get("state_code")
        log_detail = response_data.get("log_detail")
        raise Exception(f"文档清空失败！错误码：{state_code}\n日志信息：{log_detail}")
    print('---------------------------------')
