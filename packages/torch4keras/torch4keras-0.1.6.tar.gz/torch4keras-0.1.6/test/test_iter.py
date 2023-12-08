#! -*- coding: utf-8 -*-
# continue pretrain

from bert4torch.snippets import sequence_padding
import torch.nn as nn
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
import torch
from bert4torch.snippets import IterDataset, DottableDict
from bert4torch.tokenizers import Tokenizer
from glob import glob


# 基本参数
args = DottableDict()
args.data_path = 'E:/Github/MedicalGPT/data/pretrain/**/*.txt'
args.batch_size = 10
args.max_seq_length = 128

dict_path = 'E:/pretrain_ckpt/bert/chinese_L-12_H-768_A-12/vocab.txt'
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 加载数据集, 数据量较大使用IterDataset
class MyDataset(IterDataset):
    @staticmethod
    def load_data(filenames):
        """加载数据，并尽量分为不超过maxlen的句子
        """
        D = []
        for filename in filenames:
            with open(filename, encoding='utf-8') as f:
                for l in f:
                    input_ids = tokenizer.encode(l)[0]
                    if len(input_ids) > 0:
                        input_ids = input_ids[:-1]
                    if len(D) + len(input_ids) > args.max_seq_length-1:  # +当前输入超长的话，则返回之前的累计输入
                        yield D
                        D = input_ids
                    else:
                        D.extend(input_ids)

def collate_fn(batch_token_ids):
    batch_token_ids = torch.tensor(sequence_padding(batch_token_ids, value=tokenizer.pad_token_id), dtype=torch.long)
    return [batch_token_ids], batch_token_ids

file_list = glob(args.data_path, recursive=True) * 100
train_dataloader = DataLoader(MyDataset(file_list), batch_size=args.batch_size, collate_fn=collate_fn) 

count = 0
for batch in train_dataloader:
    count += 1
    if count % 100 == 0:
        print(count)
print('done')