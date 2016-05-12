from __future__ import division

import logging
import os

import csv

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from string import punctuation

logger = logging.getLogger(__name__)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

class SentimentAnalyzer(object):

    def __init__(self):
        self.afin_path = "AFINN-111.tsv"
        self.mapping = {}
        self._init_afin()

    def _init_afin(self):
        with open(os.path.join(__location__, 'AFINN-111.tsv')) as afin:
            reader = csv.reader(afin, delimiter="\t")
            for row in reader:
                word = row[0]
                sentiment = int(row[1])
                if self.mapping.get(word):
                    logger.error("The mapping already has the word: {}".format(word))
                else:
                    self.mapping[word] = sentiment
        logger.debug("sentiment mapping set up!")

    def calculate(self, word):
        return self.mapping.get(word, 0)

    def generate_mapping(self, blob):
        if not isinstance(blob, basestring):
            logger.error("Expected a string (representing a tweet).")
            return {}

        words = blob.split()
        ret = {}
        for word in words:
            word = word.lower()
            word = stemmer.stem(word)
            if word not in stop_words:
                word = "".join(w for w in word if w not in punctuation)
            ret[word] = self.calculate(word)

        return ret
