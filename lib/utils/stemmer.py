import string
import csv
import re

class Stemmer:
    def __init__(self):
        self.kbbi = self.read_dict('lib/data/kata_dasar_kbbi.csv')
        self.inflectional_suffix_3 = ['lah', 'tah', 'kah', 'pun', 'nya']
        self.inflectional_suffix_2 = ['ku', 'mu', 'in', "'y", "'a", 'ny', "'x"]
        self.inflectional_suffix_1 = ['x', 'y']
        self.derivation_suffix_1 = ['i']
        self.derivation_suffix_2 = ['an']
        self.derivation_suffix_3 = ['kan']
        self.basic_prefix = ['di', 'ke', 'se']
        self.vowels = ['a', 'i', 'u', 'e', 'o']

    def is_digit(self, token):
        return any(char.isdigit() for char in token)

    def is_punct(self, token):
        return any(char in string.punctuation for char in token)

    def read_dict(self, DATA_KBBI):
        with open(DATA_KBBI, 'r') as f_kbbi:
            kbbi = list(csv.reader(f_kbbi))
        return kbbi

    def search_kbbi(self, token):
        for elm in self.kbbi:
            if token == elm[0]:
                return True
        return False

    def remove_basic_prefix(self, token):
        if token[:2] in self.basic_prefix:
            return token[-len(token)+2:]
        return token

    def remove_inflectional_suffix(self, token):
        if token[-3:] in self.inflectional_suffix_3:
            if self.search_kbbi(token[:-3]):
                return token[:-3]
            elif self.search_kbbi(self.remove_derivation_suffix(token[:-3])):
                return self.remove_derivation_suffix(token[:-3])
        elif token[-2:] in self.inflectional_suffix_2:
            if self.search_kbbi(token[:-2]):
                return token[:-2]
            elif self.search_kbbi(self.remove_derivation_suffix(token[:-2])):
                return self.remove_derivation_suffix(token[:-2])
        elif token[-1:] in self.inflectional_suffix_1:
            if self.search_kbbi(token[:-1]):
                return token[:-1]
            elif self.search_kbbi(self.remove_derivation_suffix(token[:-1])):
                return self.remove_derivation_suffix(token[:-1])
        return token

    def remove_derivation_suffix(self, token):
        if token[-1:] in self.derivation_suffix_1:
            return token[:-1]
        elif token[-2:] in self.derivation_suffix_2:
            if self.search_kbbi(token[:-3]) and token[-3:] in self.derivation_suffix_3:
                return token[:-3]
            elif self.search_kbbi(token[:-2]):
                return token[:-2]
        if token[-3:] in self.derivation_suffix_3:
            return token[:-3]
        elif token[-2:] in self.derivation_suffix_2:
            return token[:-2]
        return token

    def banned_combi(self, token):
        if token[:2] == 'be' and token[-1:] == 'i':
            return True
        elif token[:2] == 'di' and token[-2:] == 'an':
            return True
        elif token[:2] == 'ke' and (token[-1:] == 'i' or token[-3:] == 'kan'):
            return True
        elif token[:2] == 'me' and token[-2:] == 'an':
            return True
        elif token[:2] == 'se' and (token[-1:] == 'i' or token[-3:] == 'kan'):
            return True
        return False

    def decode_ber(self, token):
        if token[3] in self.vowels:
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
            else:
                return token
        else:
            if self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
            else:
                return token

    def decode_ter(self, token):
        if token[3] in self.vowels:
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
        else:
            if self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
        return token

    def decode_me(self, token):
        if token[:5] == 'mempe':
            if self.search_kbbi(token[-len(token)+5:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+5:])):
                return token[-len(token)+5:]
        elif token[:4] == 'meng':
            if token[4] in self.vowels:
                if self.search_kbbi('k'+token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix('k'+token[-len(token)+4:])):
                    return 'k'+token[-len(token)+4:]
                elif self.search_kbbi(token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+4:])):
                    return token[-len(token)+4:]
                if token[4] == 'e':
                    if self.search_kbbi(token[-len(token)+5:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+5:])):
                        return token[-len(token)+5:]
            else:
                if self.search_kbbi(token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+4:])):
                    return token[-len(token)+4:]
        elif token[:4] == 'meny':
            if token[4] in self.vowels:
                if self.search_kbbi('s'+token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix('s'+token[-len(token)+4:])):
                    return 's'+token[-len(token)+4:]
                elif self.search_kbbi(token[-len(token)+5:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+5:])):
                    return token[-len(token)+5:]
        elif token[:4] == 'memp':
            if self.search_kbbi(token[-len(token)+3]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
        elif token[:3] == 'mem':
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
            elif self.search_kbbi('p'+token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix('p'+token[-len(token)+3:])):
                return 'p'+token[-len(token)+3:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
        elif token[:3] == 'men':
            if token[3] in self.vowels:
                if self.search_kbbi('t'+token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix('t'+token[-len(token)+3:])):
                    return 't'+token[-len(token)+3:]
                elif self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                    return token[-len(token)+2:]
            else:
                if self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                    return token[-len(token)+3:]
        elif token[:2] == 'me':
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
        else:
            return token
        return token

    def decode_pe(self, token):
        if token[:4] == 'peng':
            if token[4] in self.vowels:
                if self.search_kbbi('k'+token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix('k'+token[-len(token)+4:])):
                    return 'k'+token[-len(token)+4:]
                if self.search_kbbi(token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+4:])):
                    return token[-len(token)+4:]
                if token[4] == 'e':
                    if self.search_kbbi(token[-len(token)+5:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+5])):
                        return token[-len(token)+5:]
            else:
                if self.search_kbbi(token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+4:])):
                    return token[-len(token)+4:]
        elif token[:4] == 'peny':
            if self.search_kbbi('s'+token[-len(token)+4:]) or self.search_kbbi(self.decode_suffix('s'+token[-len(token)+4:])):
                    return 's'+token[-len(token)+4:]
        elif token[:3] == 'per':
            if token[3] in self.vowels:
                if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                    return token[-len(token)+2:]
                elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                    return token[-len(token)+3:]
            else:
                if self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                    return token[-len(token)+3:]
        elif token[:3] == 'pem':
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
            elif self.search_kbbi('p'+token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix('s'+token[-len(token)+3:])):
                    return 'p'+token[-len(token)+3:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                    return token[-len(token)+3:]
        elif token[:3] == 'pen':
            if token[3] in self.vowels:
                if self.search_kbbi('t'+token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix('t'+token[-len(token)+3:])):
                    return 't'+token[-len(token)+3:]
            elif self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                    return token[-len(token)+2:]
        elif token[:3] == 'pel':
            if token == 'pelajar':
                return token
            elif self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]
        elif token[:2] == 'pe':
            if self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]
        return token

    def decode_ny(self, token):
        if token[2] in self.vowels:
            if self.search_kbbi('s'+token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix('s'+token[-len(token)+2:])):
                return 's'+token[-len(token)+2:]
            elif self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                return token[-len(token)+3:]

    def decode_ng(self, token):
        if token[2] in self.vowels:
            if token[2] == 'e':
                if self.search_kbbi(token[-len(token)+3:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+3:])):
                    return token[-len(token)+3:]
            if self.search_kbbi('k'+token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix('k'+token[-len(token)+2:])):
                return 'k'+token[-len(token)+2:]
            elif self.search_kbbi(token[-len(token)+2:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+2:])):
                return token[-len(token)+2:]

    def decode_n(self, token):
        if token[1] in self.vowels:
            if self.search_kbbi('t'+token[-len(token)+1:]) or self.search_kbbi(self.decode_suffix('t'+token[-len(token)+1:])):
                return 't'+token[-len(token)+1:]
            elif self.search_kbbi(token[-len(token)+0:]) or self.search_kbbi(self.decode_suffix(token[-len(token)+0:])):
                return token[-len(token)+0:]

    def decode_prefix(self, token):
        if token[:3] == 'ber':
            return self.decode_ber(token)
        elif token[:3] == 'ter':
            return self.decode_ter(token)
        elif token[:2] == 'me':
            return self.decode_me(token)
        elif token[:2] == 'pe':
            return self.decode_pe(token)
        elif token[:2] == 'ny':
            return self.decode_ny(token)
        elif token[:2] == 'ng':
            return self.decode_ng(token)
        elif token[:1] == 'n':
            return self.decode_n(token)
        else:
            return token

    def decode_suffix(self, token):
        temp_token = self.remove_inflectional_suffix(token)
        if token == temp_token:
            temp_token = self.remove_derivation_suffix(token)
        return temp_token

    def is_plural(self, token):
        matches = re.match(r'^(.*)-(.*)$', token)
        if matches:
            return True
        return False

    def stemming_plural(self, plural):
        matches = re.match(r'^(.*)-(.*)$', plural)
        if matches:
            word1 = matches.group(1)
            word2 = matches.group(2)

            if word2 in self.inflectional_suffix_1 or word2 in self.inflectional_suffix_2 or word2 in self.inflectional_suffix_3:
                matches = re.match(r'^(.*)-(.*)$', word1)
                if matches:
                    word1 = matches.group(1)
                    word2 = matches.group(2)

        stem1 = self.stemming_singular(word1)
        stem2 = self.stemming_singular(word2)

        if stem1==stem2:
            return stem1
        else:
            return plural

    def stemming_singular(self, token):
        if self.search_kbbi(token):
            return token

        if self.search_kbbi(self.remove_inflectional_suffix(token)):
            return self.remove_inflectional_suffix(token)

        if self.search_kbbi(self.remove_derivation_suffix(token)):
            return self.remove_derivation_suffix(token)

        if self.search_kbbi(self.remove_basic_prefix(self.remove_inflectional_suffix(token))):
            return self.remove_basic_prefix(self.remove_inflectional_suffix(token))

        if self.search_kbbi(self.remove_basic_prefix(self.remove_derivation_suffix(token))):
            return self.remove_basic_prefix(self.remove_derivation_suffix(token))

        decode_count = 0
        while True:
            # if self.banned_combi(token):
            #     return token
            if decode_count == 3:
                return token
            if self.is_digit(token):
                return token
            if self.is_punct(token):
                return token
            if self.search_kbbi(token):
                return token
            try:
                token_temp = self.decode_prefix(token)
            except:
                return token
            if token == token_temp:
                try:
                    token_temp_basic = self.decode_prefix(self.remove_basic_prefix(token))
                except:
                    return token
                if token == token_temp_basic:
                    return token
                else:
                    if self.search_kbbi(self.remove_inflectional_suffix(token_temp_basic)):
                        return self.remove_inflectional_suffix(token_temp_basic)
                    if self.search_kbbi(self.remove_derivation_suffix(token_temp_basic)):
                        return self.remove_derivation_suffix(token_temp_basic)
                    token = token_temp_basic
                    decode_count += 1
            else:
                if self.search_kbbi(self.remove_inflectional_suffix(token_temp)):
                    return self.remove_inflectional_suffix(token_temp)
                if self.search_kbbi(self.remove_derivation_suffix(token_temp)):
                    return self.remove_derivation_suffix(token_temp)
                token = token_temp
                decode_count += 1

        return token

    def stemming(self, token):
        if self.is_plural(token):
            return self.stemming_plural(token)
        else:
            return self.stemming_singular(token)

if __name__ == '__main__':
    ST = Stemmer()
    token = ['tungguin', 'nyambi', 'kabin', 'nyakitin', 'ngejual', 'ngaji', 'ngebeliin', 'Casio', 'nunggu', 'nitipin', 'terabaikan', 'mengakalix', 'USA', 'apany', "jual'y", 'berkata-kata', 'berjual-jualan', 'barang-barang-nya', 'nunjuk-nunjukin', 'kayu-bukalapak']
    for tok in token:
        print(tok, ST.stemming(tok))
    # print (ST.remove_inflectional_suffix('curangan'))
    # print (ST.remove_derivation_suffix('abaikan'))
    # print (ST.stemming('menegur'))
    # print (ST.search_kbbi(ST.remove_derivation_suffix('tangani')))
    # print (ST.decode_suffix('layanannya'))
    # print (ST.stemming_plural('berkata-hehe'))
