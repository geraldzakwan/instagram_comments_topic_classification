import re
from nltk.tokenize import word_tokenize
from nltk.tokenize.casual import TweetTokenizer

RE_BASIC = {
    'RE_EMAIL' : r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
    'RE_MENTION' : r'@\w+',
    'RE_TRANSACTION' : r'(1[89]|[2-9][0-9])\d{10}',
    'RE_TWITTER_LINK' : r'https:\/\/t\.co[^\s]+',
    'RE_INVOICE' : r'bl\d{2}\w{8}\D{3}',
    'RE_NON_ASCII' : r'[^\x00-\x7F]+',
    'RE_TICKET' : r'#\d{7,}',
    'RE_TICKETV2' : r'tiket\w*\s\d{7,}',
    'RE_URL' : r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})',
    'RE_TAG' : r'<[^>]+>'
}


RE_RESI = {
  'RESI_GOJEK': r'^GK-\d+',
  'RESI_NINJAVAN': r'^NVID\w+',
  'RESI_NINJAVAN2': r'^NVIDBLAPK\w+',
  'RESI_JNT1': r'^888[0-9]{9}$', # 12 chars, eg: 888000118437
  'RESI_JNT2': r'^10[0-9]{8}$', # 10 chars, eg: 1002131721
  'RESI_JNT3': r'^J[A-Z]{1}[0-9]{10}$', # 12 chars, eg: JA0329239022
  'RESI_TIKI': r'^0[236][0-9]{10}$', # 12 chars, eg: 031010101010
  'RESI_RPX': r'^[157][0-9]{11}$', # 12 chars, eg: 155544446666
  'RESI_WAHANA': r'^88[0-9]{11}$', # 13 chars, eg: 8800500004444
  'RESI_POS1': r'^[A-Z0-9]{7}[A-Z]{2}[0-9]{6}$', # 15 chars, eg: 12150C1QI000001
  'RESI_POS2': r'^DEF[0-9]{12}$', # 15 chars, eg: DEF123456789012
  'RESI_POS3': r'^[0-9]{11}$', # 11 chars, eg: 10051231213
  'RESI_WAHANA2': r'^[A-Z]{3}[0-9]{5}$', # 8 chars, eg: AAA44143
  'RESI_SICEPAT': r'^[0-9]{1,12}$', # up to 12 chars, eg: 3019545
  'RESI_JNE1': r'^[A-Z]{3}[A-Z0-9]{2}[0-9]{11}$', # 16 chars, eg: CGKA000011112222
  'RESI_JNE2': r'^[12348][0-9]{12}$', # 13 chars, eg: 2123123434566
  'RESI_JNE3': r'^[0-9]{14,16}$', # 14 to 16 chars, eg: 0111211501568843
  'RESI_GRAB': r'^BLG[A-Z0-9]{13}$', # 16 char, eg: BLGEH2K5LSD82KFJ
  'RESI_GRAB2': r'^[0-9]{15}$', # 15 char, eg: 521485435102344 
  'RE_NUMBER' : r'\d+'
}

def replace_all(doc):
    doc = doc.lower()
    for key in RE_BASIC:
        doc = re.sub(RE_BASIC[key], key, doc)
    for key in RE_RESI:
        doc = re.sub(RE_RESI[key], key, doc)
    return doc

def tokenize(doc_ra):
    try:
        token = TweetTokenizer().tokenize(doc_ra)
    except:
        token = word_tokenize(doc_ra)
    return token

        
if __name__ == '__main__':
    doc = 'min JANGAN gitu 1234 @bukabantuan'
    # print (replace_all(doc))
    print (doc[-(len(doc)-2):])