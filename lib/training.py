import os
import pickle

import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from dotenv import load_dotenv
load_dotenv()

class Training():
    def __init__(self):
        self.classifier = os.getenv('TRAINING_CLASSIFIER')

    def preprocess_corpus(self, corpus):
        pass

    def build_train_data(self, corpus):
        X = []
        Y = []

        for i in range(0, 10):
            if(i % 2):
                X.append([0.1, 0.1, 0.1])
                Y.append(1.0)
            else:
                X.append([0.0, 0.0, 0.0])
                Y.append(0.0)

        return np.array(X), np.array(Y)

    def train(self, corpus):
        X, Y = self.build_train_data(corpus)

        seed = 7
        test_size = 0.2
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

        model = XGBClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]

        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))

        with open('lib/model/' + self.classifier + '.pickle', 'wb') as outfile:
            pickle.dump(model, outfile)

if __name__ == '__main__':
    training = Training()
    training.train(None)
