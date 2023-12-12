"""
文件说明：该部分存储的是常量
"""

import json
import logging
import os
import re
import openai

# 存储index名
index_name = "docx_index"

# 获取当前脚本文件的路径
current_path = os.path.abspath(__file__)
# 获取当前脚本文件所在的目录
current_dir = os.path.dirname(current_path)
# 获取项目根目录的路径
root_dir = os.path.dirname(current_dir)
# resource目录
resource_dir = f'{root_dir}/resources'

# 项目总目录
project_dir = os.path.dirname(os.path.dirname(root_dir))

# 读取配置文件
with open(f"{project_dir}/config.json", 'r', encoding='utf-8') as f:
    config_setting = dict(json.load(f))

# 读取问句模板
patterns = []
question_template = []
patternsLen = 0
with open(f'{resource_dir}/question_regex.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        question_template.append(line)
for i, line in enumerate(question_template):
    patterns.append(re.compile(line))
patternsLen = len(patterns)

# 文件切分配置
chunk_overlap = 20
min_single_para_len = 80
max_para_len = 1000
max_chunk_len = 500

# 检索方法
search_select = config_setting["search_select"]

# chatGPT的配置参数
answer_generation_model = config_setting['answer_generation_model']
openai.api_key = config_setting['openai']['api_key']
openai.api_base = config_setting['openai']['url']
