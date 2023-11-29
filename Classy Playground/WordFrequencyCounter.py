'''  Word Frequency Counter  '''


class WordFrequencyCounter:
    def __init__(self):
        self.frequencies = {}

    def count(self, text):
        tokens = text.split()
        for token in tokens:
            if token not in self.frequencies:
                self.frequencies[token] = 1
            else:
                self.frequencies[token] += 1

    def query_frequency(self, word):
        if word in self.frequencies:
            return self.frequencies[word]


wfc = WordFrequencyCounter()
wfc.count("Hello world")

print(wfc.query_frequency('world'))