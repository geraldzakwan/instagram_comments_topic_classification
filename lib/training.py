import os
import pickle

import numpy as np
import pandas as pd

import normnorm_v1 as NN

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.feature_extraction.text import TfidfVectorizer

from dotenv import load_dotenv
load_dotenv()

class Training():
    def __init__(self):
        self.path_or_url = os.getenv('PATH_OR_URL')
        self.model_name = os.getenv('TRAINING_FEATURE') + '_' + os.getenv('TRAINING_CLASSIFIER') + '_' + os.getenv('TRAINING_DETAIL')
        self.normalization = NN.Normnorm()

    # Expecting Google sheet url or CSV file
    def build_corpus(self):
        list_of_sentence = []
        list_of_label = []

        if 'www' in self.path_or_url:
            pass
        else:
            label_dict = {}

            with open('lib/corpus/' + self.path_or_url + '/metadata.txt', 'r') as infile:
                for line in infile:
                    label_string, label_float = line.split()
                    label_dict[label_string] = float(label_float)

            data = pd.read_csv('lib/corpus/' + self.path_or_url + '/data.csv', delimiter=';')

            for sentence in data['sentence']:
                list_of_sentence.append(sentence.lower())

            for label in data['label']:
                list_of_label.append(label_dict[label])

        return list_of_sentence, list_of_label

    def preprocess_corpus(self, corpus_data):
        preprocessed_corpus_data = []

        for sentence in corpus_data:
            preprocessed_corpus_data.append(self.normalization.norm(sentence))

        return preprocessed_corpus_data

    # Return the extracted feature (TFIDF/w2v) from corpus
    def build_train_data(self, corpus_data, corpus_label):
        if 'tfidf' in self.model_name:
            # Ignore terms which appear in more than 80% of the total sentence
            # Ignore terms which appear in less than 5 sentence
            if('test' in self.path_or_url):
                tfidfconverter = TfidfVectorizer()
            else:
                tfidfconverter = TfidfVectorizer(min_df=5, max_df=0.8)

            X = tfidfconverter.fit_transform(corpus_data).toarray()

            with open('lib/model/' + self.path_or_url + '/tfidf.pickle', 'wb') as outfile:
                pickle.dump(tfidfconverter, outfile)
        elif 'w2v' in self.model_name:
            # TO-DO: Need to save word2vec txt file as well to load later if needed
            pass

        return np.array(X), np.array(corpus_label)

    def train(self):
        corpus_data, corpus_label = self.build_corpus()
        corpus_data = self.preprocess_corpus(corpus_data)
        X, Y = self.build_train_data(corpus_data, corpus_label)

        if(len(X) > 100):
            seed = 7
            test_size = 0.2
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

            model = XGBClassifier()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            predictions = [round(value) for value in y_pred]

            accuracy = accuracy_score(y_test, predictions)
            print("Accuracy: %.2f%%" % (accuracy * 100.0))

        model = XGBClassifier()
        model.fit(X, Y)

        with open('lib/model/' + self.path_or_url + '/' + self.model_name + '.pickle', 'wb') as outfile:
            pickle.dump(model, outfile)

if __name__ == '__main__':
    training = Training()
    training.train()
