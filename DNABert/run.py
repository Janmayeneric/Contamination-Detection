import argparse
from transformers import  AutoTokenizer, AdamW, get_linear_schedule_with_warmup, BertModel
import torch
import torch.nn as nn
from tqdm import tqdm
import numpy as np
from torch.utils.data import DataLoader, Dataset


def read_fastq(filename):
    cur_read = []
    with open(filename, "r", encoding="utf-8") as fr:
        for line in fr:
            cur_read.append(line)

            if len(cur_read) == 4:
                yield "".join(cur_read)
                cur_read = []


parser = argparse.ArgumentParser()

parser.add_argument('--train_file', type=str, default="1000-0.1.fastq", help='training fastq file')
parser.add_argument('--test_file', type=str, default="1000-0.05.fastq")
parser.add_argument('--batch_size', type=int, default=64, help='batch size')

args = parser.parse_args()


class Model(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = BertModel.from_pretrained("armheb/DNA_bert_6")

        self.hidden_size = 768
        self.dropout = nn.Dropout(0.1)

        self.classifier = nn.Linear(self.hidden_size, 1)

        self.loss = torch.nn.BCEWithLogitsLoss()

    def forward(self, input_ids, attention_mask, labels=None, **kwargs):
        outputs = self.model(input_ids, attention_mask)["last_hidden_state"][:, 0, :]

        sequence_output = self.dropout(outputs)
        logits = self.classifier(sequence_output)

        loss = None
        if labels is not None:
            labels = labels.float()
            loss = self.loss(logits.view(-1, 1), labels.view(
                -1, 1))

        return loss, logits


class CustomDataset(Dataset):
    def __init__(self, ds):
        self.dataset = ds

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        return self.dataset[idx]


def process_data(tokenizer, file):
    max_length = 150

    data = []
    for _read in tqdm(read_fastq(file)):
        fastq_read = _read.split("\n")[1]
        read_label = _read.split("\n")[0]

        input_ids = []

        input_ids.append(tokenizer.convert_tokens_to_ids("[CLS]"))
        for i in range(len(fastq_read) - 5):
            input_ids.append(tokenizer.convert_tokens_to_ids(fastq_read[i:i + 6]))
            if len(input_ids) == max_length - 1:
                break
        input_ids.append(tokenizer.convert_tokens_to_ids("[SEP]"))

        attention_mask = [1 for _ in range(len(input_ids))]
        while len(attention_mask) < max_length:
            attention_mask.append(0)
            input_ids.append(0)

        data.append([np.array(input_ids), np.array(attention_mask),
                     np.array([1 if read_label.startswith("@SRR6756023") else 0])])

    return CustomDataset(data)


def evaluate(model, dataloader):
    nums_1, nums_0 = 0, 0
    acc_1, acc_0 = 0, 0

    for batch in tqdm(dataloader):
        input_ids = torch.Tensor(batch[0]).long().cuda()
        attention_mask = torch.Tensor(batch[1]).long().cuda()

        labels = torch.Tensor(batch[2]).long().view(-1).tolist()
        logits = model(input_ids, attention_mask)[1]
        _predictions = torch.sigmoid(logits).view(-1).cpu().tolist()
        print(_predictions[:10])
        predictions = [1 if _p > 0.5 else 0 for _p in _predictions]

        for p, t in zip(predictions, labels):
            if t == 0:
                if p == 0:
                    acc_0 += 1
                nums_0 += 1
            if p == 0:
                if t == 0:
                    acc_1 += 1
                nums_1 += 1

    recall = acc_0 / nums_0
    precision = acc_1 / nums_1
    print("Precision: {}".format(precision))
    print("Recall: {}".format(recall))
    print("f1: {}".format(2 * (precision * recall) / (precision + recall)))


def main():
    tokenizer = AutoTokenizer.from_pretrained("armheb/DNA_bert_6")

    model = Model()
    model.cuda()
    # AutoModelForSequenceClassification.from_pretrained("armheb/DNA_bert_6")
    # config = BertConfig.from_pretrained("armheb/DNA_bert_6")
    # config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512)
    # model = BertForSequenceClassification(config)

    train_dataset = process_data(tokenizer, args.train_file)  # , process_data(tokenizer)
    test_dataset_05 = process_data(tokenizer, "1000-0.05.fastq")
    test_dataset_10 = process_data(tokenizer, "1000-0.1.fastq")
    test_dataset_20 = process_data(tokenizer, "1000-0.2.fastq")

    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=args.batch_size)
    test_dataloader_05 = DataLoader(test_dataset_05, shuffle=False, batch_size=128)
    test_dataloader_10 = DataLoader(test_dataset_10, shuffle=False, batch_size=128)
    test_dataloader_20 = DataLoader(test_dataset_20, shuffle=False, batch_size=128)

    optimizer = AdamW(model.parameters(), 0.0001)
    scheduler = get_linear_schedule_with_warmup(optimizer, 100, 5000)

    for epoch in range(3):
        model.train()
        epoch_loss = 0
        num_steps = 0
        for batch in tqdm(train_dataloader):
            input_ids = torch.Tensor(batch[0]).long().cuda()
            attention_mask = torch.Tensor(batch[1]).long().cuda()
            labels = torch.Tensor(batch[2]).long().cuda()
            loss = model(input_ids, attention_mask, labels=labels)[0]

            epoch_loss += loss.item()
            num_steps += 1

            loss.backward()
            optimizer.step()
            scheduler.step()

        print("epoch: {}, Update Steps {}, loss: {}\n".format(epoch, num_steps, epoch_loss / num_steps))
        with torch.no_grad():
            model.eval()
            evaluate(model, test_dataloader_05)
            evaluate(model, test_dataloader_10)
            evaluate(model, test_dataloader_20)


main()
