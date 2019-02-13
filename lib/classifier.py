import os
import pickle
import normnorm_v1 as NN

from dotenv import load_dotenv
load_dotenv()

class Classifier():
    def __init__(self):
        self.path_or_url = os.getenv('PATH_OR_URL')
        self.model_name = os.getenv('SERVING_FEATURE') + '_' + os.getenv('SERVING_CLASSIFIER') + '_' + os.getenv('SERVING_DETAIL')

        with open('lib/model/' + self.path_or_url + '/' + os.getenv('SERVING_FEATURE') + '.pickle', 'rb') as infile:
            self.feature_extractor = pickle.load(infile)

        with open('lib/model/' + self.path_or_url + '/' + self.model_name + '.pickle', 'rb') as infile:
            self.classifier = pickle.load(infile)

        self.label_dict = {}

        with open('lib/corpus/' + self.path_or_url + '/metadata.txt', 'r') as infile:
            for line in infile:
                label_string, label_float = line.split()
                self.label_dict[label_string] = float(label_float)

        self.normalization = NN.Normnorm()

    def preprocess_text(self, text):
        return self.normalization.norm(text)

    def extract_feature(self, text):
        return self.feature_extractor.transform([text])

    def get_class(self, text):
        text = self.preprocess_text(text)
        label_float = self.classifier.predict(self.extract_feature(text)[0])

        for label in self.label_dict:
            if self.label_dict[label] == label_float:
                return label

    def get_classes(self, texts):
        labels = []

        for text in texts:
            text = self.preprocess_text(text)
            label_float = self.classifier.predict(self.extract_feature(text)[0])

            for label in self.label_dict:
                if self.label_dict[label] == label_float:
                    labels.append(label)

        return labels

if __name__ == '__main__':
    classifier = Classifier()
    print(classifier.get_class('Contoh kalimat'))
