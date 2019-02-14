import csv
import string
import utils as ut
from utils import stemmer
from utils import preprocess as pr
from nltk.corpus import words as words

ST = stemmer.Stemmer()

class Normnorm:
    def __init__(self):
        self.DATA_KBBI = ut.DATA_KBBI
        self.KORPUS_NONFORMAL = ut.KORPUS_NONFORMAL
        self.eng_dict = set(words.words())

        with open(self.DATA_KBBI, 'r') as f_kbbi:
            data_kbbi = csv.reader(f_kbbi)
            kbbi_list = list(data_kbbi)
        self.kbbi_list = kbbi_list

        with open(self.KORPUS_NONFORMAL, 'r') as f_korpus:
            data_nonformal = csv.reader(f_korpus)
            nonformal_list = list(data_nonformal)
        self.nonformal_list = nonformal_list


    def checkEnglish(self, token):
        return token in self.eng_dict

    def checkPunct(self, token):
        return token in string.punctuation

    def checkRE(self, token):
        return 'RE_' in token or 'RESI_' in token

    def checkKBBI(self, token):
        for elm in self.kbbi_list:
            if elm[0] == token:
                return True
        return False

    def checkNonformal(self, token):
        for elm in self.nonformal_list:
            if token == elm[0]:
                return True, elm[1]
        return False, token

    def checkStem(self, token):
        stem = ST.stemming(token)
        if token == stem:
            return False
        else:
            return True

    def norm(self, record):
        norms = []
        pr_replace = pr.replace_all(record)
        pr_token = pr.tokenize(pr_replace)
        for token in pr_token:
            try:
                if self.checkPunct(token):
                    norms.append(token)
                elif self.checkEnglish(token):
                    norms.append(token)
                elif self.checkKBBI(token):
                    norms.append(token)
                else:
                    check_nonformal, new_token = self.checkNonformal(token)
                    if check_nonformal:
                        norms.append(new_token)
                    elif self.checkStem(token):
                        norms.append(token)
                    else:
                        norms.append(token)
            except:
                norms.append(token)

        return ' '.join(norms)


if __name__ == '__main__':
    NN = Normnorm()
    record = "nawarnya"
    print (record)
    print (NN.norm(record))
