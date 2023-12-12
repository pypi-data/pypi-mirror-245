"""
文件说明：该部分初始化模型、搜索客户端等
"""
import torch

from FourthDimension.config import config_setting
from FourthDimension.fds.client import FdsClient
# from FourthDimension.util.fd_util import load_bge_model

def load_bge_model():
    from transformers import AutoTokenizer, AutoModel
    # Load model from HuggingFace Hub
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(config_setting['embedding_model'])
    model = AutoModel.from_pretrained(config_setting['embedding_model']).to(device)
    model.eval()
    return model, tokenizer

# embed模型
print('模型初始化...')
embed_model, embed_tokenizer = load_bge_model()
embed_model_device = next(embed_model.parameters()).device
print('模型初始化完成...')

# lucene配置
fds_client = FdsClient()



