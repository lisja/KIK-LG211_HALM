from nltk.stem import *


def stemming():
    stemmer = PorterStemmer()

    plurals = ['caresses', 'flies', 'dies', 'mules', 'denied',
            'died', 'agreed', 'owned', 'humbled', 'sized',
            'meeting', 'stating', 'siezing', 'itemization',
            'sensational', 'traditional', 'reference', 'colonizer',
            'plotted']

    singles = [stemmer.stem(plural) for plural in plurals]

    for i in singles:
        print(i)


stemming()
