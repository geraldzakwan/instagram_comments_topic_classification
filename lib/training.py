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
        self.train_dist_dict = {}

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
                    label_string, label_float, count_train = line.split()
                    label_dict[label_string] = float(label_float)
                    self.train_dist_dict[float(label_float)] = int(count_train)

            data = pd.read_csv('lib/corpus/' + self.path_or_url + '/data.tsv', delimiter='\t')

            for sentence in data['sentence']:
                list_of_sentence.append(sentence.lower())

            for label in data['label']:
                list_of_label.append(label_dict[label])

        return list_of_sentence, list_of_label

    # Expecting Google sheet url or CSV file
    def build_test_corpus(self):
        list_of_sentence = []
        list_of_label = []

        if 'www' in self.path_or_url:
            pass
        else:
            label_dict = {}

            with open('lib/corpus/' + self.path_or_url + '/metadata.txt', 'r') as infile:
                for line in infile:
                    label_string, label_float, count_train = line.split()
                    label_dict[label_string] = float(label_float)
                    self.train_dist_dict[float(label_float)] = int(count_train)

            data = pd.read_csv('lib/corpus/' + self.path_or_url + '/test_data.tsv', delimiter='\t')

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

    def build_train_data(self, corpus_data, corpus_label):
        train_data = []
        train_label = []

        for i in range(0, len(corpus_data)):
            if(self.train_dist_dict[corpus_label[i]] > 0):
                train_data.append(corpus_data[i])
                train_label.append(corpus_label[i])

                self.train_dist_dict[corpus_label[i]] = self.train_dist_dict[corpus_label[i]] - 1

        return train_data, train_label

    # Return the extracted feature (TFIDF/w2v) from corpus
    def convert_train_data_to_features(self, corpus_data, corpus_label):
        if 'tfidf' in self.model_name:
            # Ignore terms which appear in more than 80% of the total sentence
            # Ignore terms which appear in less than 5 sentence
            if('test' in self.path_or_url):
                self.tfidfconverter = TfidfVectorizer()
            else:
                self.tfidfconverter = TfidfVectorizer(min_df=5, max_df=0.8)

            X = self.tfidfconverter.fit_transform(corpus_data).toarray()

            with open('lib/model/' + self.path_or_url + '/tfidf.pickle', 'wb') as outfile:
                pickle.dump(self.tfidfconverter, outfile)
        elif 'w2v' in self.model_name:
            # TO-DO: Need to save word2vec txt file as well to load later if needed
            pass

        return np.array(X), np.array(corpus_label)

    # Return the extracted feature (TFIDF/w2v) from corpus
    def convert_test_data_to_features(self, corpus_data, corpus_label):
        if 'tfidf' in self.model_name:
            X = self.tfidfconverter.transform(corpus_data).toarray()
        elif 'w2v' in self.model_name:
            # TO-DO: Need to save word2vec txt file as well to load later if needed
            pass

        return np.array(X), np.array(corpus_label)

    def train(self):
        corpus_data, corpus_label = self.build_corpus()
        print("Build corpus done")
        corpus_data = self.preprocess_corpus(corpus_data)
        print("Preprocessing done")
        train_data, train_label = self.build_train_data(corpus_data, corpus_label)
        print("Build training data done")
        X, Y = self.convert_train_data_to_features(train_data, train_label)

        # if(len(X) > 100):
        #     seed = 7
        #     test_size = 0.2
        #     X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
        #
        #     model = XGBClassifier()
        #     model.fit(X_train, y_train)
        #
        #     y_pred = model.predict(X_test)
        #     predictions = [round(value) for value in y_pred]
        #
        #     accuracy = accuracy_score(y_test, predictions)
        #     print("Accuracy: %.2f%%" % (accuracy * 100.0))

        self.model = XGBClassifier()
        self.model.fit(X, Y)

        if(len(X) > 100):
            Y = self.model.predict(X)
            predictions = [round(value) for value in Y]

            accuracy = accuracy_score(Y, predictions)
            print("Train accuracy: %.2f%%" % (accuracy * 100.0))

        with open('lib/model/' + self.path_or_url + '/' + self.model_name + '.pickle', 'wb') as outfile:
            pickle.dump(self.model, outfile)

    def test(self):
        test_data, test_label = self.build_test_corpus()
        print("Build corpus done")
        test_data = self.preprocess_corpus(test_data)
        print("Preprocessing done")
        X_test, Y_test = self.convert_test_data_to_features(test_data, test_label)

        Y_pred = self.model.predict(X_test)
        predictions = [round(value) for value in Y_pred]

        accuracy = accuracy_score(Y_test, predictions)
        print("Test accuracy: %.2f%%" % (accuracy * 100.0))

if __name__ == '__main__':
    training = Training()
    training.train()
    training.test()
