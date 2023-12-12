import hashlib
import re
from typing import List

import faiss
import jieba
import numpy as np
import tiktoken
import torch


from FourthDimension.config import patternsLen, patterns, config_setting
from FourthDimension.config.config import embed_model
from FourthDimension.docstore.document import FDDocument


def get_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(tiktoken.get_encoding("cl100k_base").encode(string))
    return num_tokens


def replace_multiple_newlines(text: str) -> str:
    pattern = r'\n{1,}'  # 匹配连续一个以上的换行符
    replacement = '\n'  # 替换为一个换行符
    updated_text = re.sub(pattern, replacement, text)
    return updated_text





def get_embedding(sentence):
    import torch
    from FourthDimension.config.config import embed_model as model
    from FourthDimension.config.config import embed_tokenizer as tokenizer
    from FourthDimension.config.config import embed_model_device as device
    encoded_input = tokenizer([sentence], padding=True, truncation=True, return_tensors='pt', max_length=512)
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(input_ids=encoded_input['input_ids'].to(device),
                             token_type_ids=encoded_input['token_type_ids'].to(device),
                             attention_mask=encoded_input['attention_mask'].to(device))
        # Perform pooling. In this case, cls pooling.
        sentence_embeddings = model_output[0][:, 0]
    # normalize embeddings
    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    # print("Sentence embeddings:", sentence_embeddings.tolist()[0])
    return sentence_embeddings[0].tolist()


def compute_sha1_from_file(file_path):
    with open(file_path, "rb") as file:
        bytes = file.read()
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash


def compute_sha1_from_content(content):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash


# 问题处理
def question_analysis(question):
    find = False
    query = question.replace("，", "")
    matchIndex = []
    for i in range(patternsLen):
        regex = patterns[i]
        matcher = re.search(regex, query)
        if matcher is not None:
            find = True
            for match in re.finditer(regex, query):
                start = match.start()
                end = match.end()
                matchIndex.append([start, end])
    if find:
        mergeIndex = merge(matchIndex)
        res = []
        startI = 0
        for i in range(len(mergeIndex)):
            if startI != mergeIndex[i][0]:
                res.append(query[startI:mergeIndex[i][0]])
            startI = mergeIndex[i][1]
        if mergeIndex[-1][1] < len(query):
            res.append(query[mergeIndex[-1][1]:])
        return ''.join(res)
    return query


def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for i in range(len(intervals)):
        l, r = intervals[i][0], intervals[i][1]
        if len(res) == 0 or res[-1][1] < l:
            res.append([l, r])
        else:
            res[-1][1] = max(res[-1][1], r)
    return res


def text_vector_rerank(question: str,
                       fd_documents: List[FDDocument]
                       ) -> List[FDDocument]:
    """
    根据 chunk 对应自然段集合，对 fd_documnets 进行重排
    Args:
        question: 问题
        fd_documents: 文档列表

    Returns: 重排后的fd_documents列表

    """
    chunk_scores = []
    for i, fd_document in enumerate(fd_documents):
        para_contexts: list = fd_document.get_para_contexts()
        para_contexts_ = "".join(para_contexts)
        # 自然段集合进行分句
        sents = chinese_segment(para_contexts_)
        sents_score = []
        # 重排
        for context in sents:
            D = get_simi_score(question, context)
            # D = 0
            sents_score.append({
                'sentence': context,
                'score': str(D[0][0])
            })
        result = [{k: float(v) if k == "score" else v for k, v in d.items()} for d in sents_score]
        sorted_dict_list = sorted(result, key=lambda x: x['score'])
        if len(sents) == 1:
            score = sum(d["score"] for d in sorted_dict_list) / len(sents)
        elif len(sents) == 2:
            score = sorted_dict_list[0]["score"] * 0.7 + sorted_dict_list[1]["score"]
        else:
            score = sorted_dict_list[0]["score"] * 0.5 + sorted_dict_list[1]["score"] * 0.3 + sorted_dict_list[2][
                "score"] * 0.2
        chunk_scores.append([i, score])
    sorted_fd_documents = sorted(chunk_scores, key=lambda x: x[1])
    rerank_fd_documents = []
    for i, d in enumerate(range(len(sorted_fd_documents))):
        index = sorted_fd_documents[i][0]
        rerank_fd_documents.append(fd_documents[index])
    return rerank_fd_documents


def chinese_segment(text):
    sentences = []
    seg_list = jieba.cut(text, cut_all=False)
    sentence = []
    for word in seg_list:
        sentence.append(word)
        if word in ['。', '？', '！']:
            sentences.append("".join(sentence))
            sentence = []
    if sentence:
        sentences.append("".join(sentence))
    return sentences

def get_simi_score(question, context):
    query_embed = get_embedding(question)
    contexts_embed = get_embedding(context)
    # D = 0
    D = index_search(query_embed=query_embed, context_embed=contexts_embed)
    return D

def index_search(query_embed, context_embed):
    contexts_embeddings = np.array([context_embed]).astype("float32")
    index = faiss.IndexFlatL2(contexts_embeddings.shape[1])  # 创建Faiss索引
    index.add(contexts_embeddings)
    query_embedding = np.array([query_embed]).astype("float32")
    D, I = index.search(query_embedding, 1)
    return D


