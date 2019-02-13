import csv
import enchant
import string
import utils as ut
from utils import stemmer
from utils import preprocess as pr
from random import randint

ST = stemmer.Stemmer()

class DPchat:
    def __init__(self):
        self.DATA_CHAT = ut.COMPLETE_CHAT
        self.DATA_TXT = ut.DATA_TXT
        self.DATASET_CUSTOMERCHAT = ut.DATASET_CUSTOMERCHAT
        self.DATASET_TOKEN = ut.DATASET_TOKEN
        self.DATA_KBBI = ut.DATA_KBBI
        self.eng_dict = enchant.Dict("en_US")
        self.DATASET_TOKEN_BAKU = ut.DATASET_TOKEN_BAKU
        self.DATASET_TOKEN_NONBAKU = ut.DATASET_TOKEN_NONBAKU
        self.DATASET_TOKEN_PUNCT = ut.DATASET_TOKEN_PUNCT
        self.DATASET_TOKEN_ENG = ut.DATASET_TOKEN_ENG


    def setChatToTxt(self):
        file_txt = open(self.DATA_TXT, 'w')
        with open(self.DATA_CHAT, 'r') as f_datachat:
            dataset = csv.reader(f_datachat)
            for dataset_row in dataset:
                if dataset_row[3][0] == 'C' and dataset_row[3][1] == 'S' and dataset_row[3][2] == ' ':
                    continue
                elif dataset_row[3] == 'BukaBantuan Chat':
                    continue
                else:
                    chat_prep = pr.replace_all(dataset_row[4])
                    file_txt.write("%s\n" % chat_prep)
        file_txt.close()

    def setCustomerChat(self):
        temp = []
        with open(self.DATA_CHAT, 'r') as f_datachat:
            dataset = csv.reader(f_datachat)
            for dataset_row in dataset:
                if dataset_row[3][0] == 'C' and dataset_row[3][1] == 'S' and dataset_row[3][2] == ' ':
                    continue
                elif dataset_row[3] == 'BukaBantuan Chat':
                    continue
                else:
                    if dataset_row[4] != '':
                        temp.append([dataset_row[4]])

        with open(self.DATASET_CUSTOMERCHAT, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t in temp:
                data_set.writerow(t)

    
    def setToken(self):
        temp = []
        count = []
        with open(self.DATASET_CUSTOMERCHAT, 'r') as f_dataset:
            dataset = csv.reader(f_dataset)
            for dataset_row in dataset:
                data_ra = pr.replace_all(dataset_row[0])
                token = pr.tokenize(data_ra)
                for elm in token:
                    if elm not in temp:
                        temp.append(elm)
                        count.append(0)
                    else:
                        count[temp.index(elm)] += 1
        
        with open(self.DATASET_TOKEN, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t, c in zip(temp, count):
                data_set.writerow([t, c])
    
    def setBakuWords(self):
        temp_baku = []
        temp_baku_eng = []
        temp_nonbaku = []
        temp_punct = []
        temp_nonbaku_baku = []

        with open(self.DATASET_TOKEN, 'r') as f_token:
            dataset_token = csv.reader(f_token)
            token_list = list(dataset_token)
        with open(self.DATA_KBBI, 'r') as f_kbbi:
            data_kbbi = csv.reader(f_kbbi)
            kbbi_list = list(data_kbbi)

        for token in token_list:
            if self.eng_dict.check(token[0]):
                temp_baku_eng.append(token)
            elif token[0] in string.punctuation:
                temp_punct.append(token)
            elif 'RE_' in token[0] or 'RESI_' in token[0]:
                temp_baku.append(token)
            else:
                a = 0
                for kbbi in kbbi_list:
                    if token[0] == kbbi[0]:
                        temp_baku.append(token)
                        a = 1
                        break
                if a == 0:
                    nonbaku_baku = ST.stemming(token[0])
                    if nonbaku_baku != token[0]:
                        temp_nonbaku_baku.append([nonbaku_baku, token[0]])
                    else:
                        temp_nonbaku_baku.append([nonbaku_baku, '0'])  
                    temp_nonbaku.append(token)
        
        with open(self.DATASET_TOKEN_BAKU, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t in temp_baku:
                data_set.writerow(t)
        with open(self.DATASET_TOKEN_NONBAKU, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t, n in zip(temp_nonbaku, temp_nonbaku_baku):
                temp_1 = t
                temp_2 = n
                temp_1.extend(temp_2)
                data_set.writerow(temp_1)
        with open(self.DATASET_TOKEN_PUNCT, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t in temp_punct:
                data_set.writerow(t)
        with open(self.DATASET_TOKEN_ENG, 'w') as f_dataset:
            data_set = csv.writer(f_dataset)
            for t in temp_baku_eng:
                data_set.writerow(t)

if __name__ == '__main__':
    DPC = DPchat()
    # DPC.setChatToTxt()
    # DPC.setCustomerChat()
    # DPC.setToken()
    DPC.setBakuWords()
