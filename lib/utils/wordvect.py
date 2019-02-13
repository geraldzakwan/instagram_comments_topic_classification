from gensim.models import FastText
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.tokenize.casual import TweetTokenizer
import re
import numpy as np

class WordTrain:
    def __init__(self, INPUT_TXT, OUTPUT_PATH_SKIPGRAM, model):
        self.INPUT_TXT = INPUT_TXT
        self.OUTPUT_PATH_SKIPGRAM = OUTPUT_PATH_SKIPGRAM
        self.model = model
        self.file_input_text = open(self.INPUT_TXT, 'r')
        self.data = self.file_input_text.readlines()
        self.data_train = [TweetTokenizer().tokenize(self.remove_tags(line.lower())) for line in self.data]
        self.tagged_data = [TaggedDocument(words=TweetTokenizer().tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(self.data)]
   
    def train(self):
        # Learn the word representation using skipgram model
        if self.model == 'FastText':
            skipgram = FastText(self.data_train, min_count=1)
        elif self.model == 'Word2Vec':
            skipgram = Word2Vec(self.data_train, min_count=1)
        elif self.model == 'Doc2Vec':
            skipgram = Doc2Vec(self.tagged_data, vector_size=100, window=2, min_count=1, workers=4)
        else:
            skipgram = Word2Vec(self.data_train, min_count=1)
        skipgram.save(self.OUTPUT_PATH_SKIPGRAM)

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)



class Skipgram:
    def __init__(self, OUTPUT_PATH_SKIPGRAM, model):
        # Load pre-trained skipgram model
        # this must be take a longer time
        self.OUTPUT_PATH_SKIPGRAM = OUTPUT_PATH_SKIPGRAM
        if model == 'FastText':
            self.skipgram = FastText.load(self.OUTPUT_PATH_SKIPGRAM)
        elif model == 'Word2Vec':
            self.skipgram = Word2Vec.load(self.OUTPUT_PATH_SKIPGRAM)
        elif model == 'Doc2Vec':
            self.skipgram = Doc2Vec.load(self.OUTPUT_PATH_SKIPGRAM)
        else:
            self.skipgram = Word2Vec.load(self.OUTPUT_PATH_SKIPGRAM)
        
    def vectoring(self, word):
        return self.skipgram[word]
    
    def vectoring_doc(self, token):
        return self.skipgram.infer_vector(token)

    def vectoring_token(self, token):
        return np.array([self.vectoring(item) if item in self.skipgram.wv.vocab else [0.0]*100 for item in token])

    def vectoring_averaging_token(self, token):
        vector = self.vectoring_token(token)
        averagies = [np.mean(vector, axis=0)]
        return averagies[0]

    def vectoring_summing_token(self, token):
        vector = self.vectoring_token(token)
        summ = [np.sum(vector, axis=0)]
        return summ[0]

    def similar_words(self, word):
        return self.skipgram.most_similar(word)

    def similar_words_first(self, word):
        return self.skipgram.most_similar(word)[0][0]
