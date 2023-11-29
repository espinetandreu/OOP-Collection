import re
import string
import nltk
import datetime
import numpy as np
import pandas as pd

# ============== TOKENIZE ===================

# Define a set of common English stopwords, compile a regex pattern for punctuation and create a Snowball stemmer for English.
STOPWORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                 'do', 'at', 'this', 'but', 'his', 'by', 'from'])
PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))


# Define functions for tokenizing, filtering punctuation, stopwords, stemming and word filter.
def tokenize(text):
    return re.split(r'\s+|\.', text)


def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]


# Define a function to analyze text using the functions just defined
def analyze_query(text):
    # AND
    matches = re.findall(r'"([^"]*)"', text)
    analysed_and_query = [word for match in matches for word in match.split()]
    # OR
    tokens = tokenize(text)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    analysed_or_query = [token for token in tokens if token not in analysed_and_query]
    return analysed_and_query, analysed_or_query


def analyze(text):
    tokens = tokenize(text)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    return [token for token in tokens if token]


# ======== GENERATE N-GRAMS ===========

def generate_ngrams(s):
    n = 3
    ngrams = []
    for i in range(len(s) - n + 1):
        ngrams.append(s[i:i + n])
    ngrams.append(s)
    return ngrams


# ======== INVERTED INDEXING SYMBOLS ==========

# Define a symbol class to represent a symbol ID and its description. (Maps ID to descriptions)
class Symbol:
    def __init__(self, ID, description):
        self.ID = ID
        self.description = description


# Define an Index class to build and search an index of symbols based on their descriptions. (Maps words/tokens to sets of symbols ID)
class Index:
    def __init__(self):
        self.index = {}  # Dictionary to hold index terms and associated symbol IDs.
        self.symbols = {}  # Dictionary to hold symbol IDs and associated symbols.

    # Index a symbol by adding its terms to the index.
    def index_symbol(self, symbol):
        # Add the symbol to the symbol dictionary if it isn't already there.
        if symbol.ID not in self.symbols:
            self.symbols[symbol.ID] = symbol
        # For each token in the symbol's description, add the symbol ID to the index's set of IDs for that token.
        for token in analyze(symbol.description):
            for gram in generate_ngrams(token):
                if gram not in self.index:
                    self.index[gram] = set()
                self.index[gram].add(symbol.ID)

    # Given an analyzed query, return the set of IDs for each term in the query.
    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]

    # Search the index for symbols that match the query.
    def search(self, query, analyzed_description):
        # Analyze the query and get the set of IDs for each term.
        analyzed_and_query, nongram_analyzed_or_query = analyze_query(query)
        analyzed_or_query = [gram for token in nongram_analyzed_or_query for gram in generate_ngrams(token)]
        and_results = self._results(analyzed_and_query)
        or_results = self._results(analyzed_or_query)
        if and_results:
            and_symbols_id = [self.symbols[doc_id].ID for doc_id in set.intersection(*and_results)]
        else:
            and_symbols_id = []

        if or_results:
            or_symbols_objects = [self.symbols[doc_id] for doc_id in set.union(*or_results)]
            scores = {}
            scores = {symbol.ID: sum(1 for token in analyzed_or_query if token in analyzed_description[symbol.ID]) for
                      symbol in or_symbols_objects if symbol.ID not in scores}
            or_symbols_id = [[symbol.ID, round(scores[symbol.ID] / len(analyzed_or_query), 2)] for symbol in
                             or_symbols_objects if
                             symbol.ID in scores and round(scores[symbol.ID] / len(analyzed_or_query), 2) >= 0.3]
        else:
            or_symbols_id = []
            return and_symbols_id, or_symbols_id

        return and_symbols_id, or_symbols_id