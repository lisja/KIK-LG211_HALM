from nltk.stem import *
from nltk.tokenize import sent_tokenize, word_tokenize

def stemming(file_path): # tokenizing the text from the file, printing the tokenized file and stemming the tokens

    stemmer = PorterStemmer()
   
    with open(file_path, "r") as file:
        text = file.read()
    words = word_tokenize(text)

    print("{0:20}{1:20}".format("Word", "Stem") )
    print()
    
    for i in words:
        print("{0:20}{1:20}".format(i, stemmer.stem(i)))


def main():

    file_path = "test_txt.txt"

    s = stemming(file_path)

main()
