import os
import pickle

from dotenv import load_dotenv
load_dotenv()

class Classifier():
    def __init__(self):
        with open('lib/model/' + os.getenv('SERVING_CLASSIFIER') + '.pickle', 'rb') as infile:
            self.classifier = pickle.load(infile)

    def preprocess_text(self, text):
        pass

    def get_class(self, text):
        label = self.classifier.predict([1.0, 1.0, 1.0])
        if label == 0.0:
            return '0'
        else:
            return '1'

if __name__ == '__main__':
    classifier = Classifier()
    print(classifier.get_class(None))
