from nltk.stem import *
from nltk.tokenize import sent_tokenize, word_tokenize
import operator

def stemming(file_path): # tokenizing the text from the file, printing the tokenized file
                         # + stemming the tokens and counting their occurrence

    stemmer = PorterStemmer()
    count_stems = dict()

    with open(file_path, "r") as file:
        text = file.read()
    words = word_tokenize(text)

    print("Printing words, stems and occurrence of each stem from a file: ")
    print()

    print("{0:20}{1:20}".format("Word", "Stem"))
    
    print("-"*40)
    print()
    
    for i in words:
        print("{0:20}{1:20}".format(i, stemmer.stem(i)))   # printing the words and their stems

        if stemmer.stem(i) in count_stems:
            count_stems[stemmer.stem(i)] += 1
        else:
            count_stems[stemmer.stem(i)] = 1

    print()    
    print("*"*40)
    print()
    
    print("{0:20}{1:20}".format("Stem", "Occurrence"))  # printing the stems and their occurrences:
                                                        # first by number of occurrences, then alphabetically
   
    print("-"*40)
    print()

    sorted_stems = sorted(count_stems.items(), key=operator.itemgetter(0))
    sorted_stems = dict(sorted(sorted_stems, key=operator.itemgetter(1), reverse=True))

    for item, amount in sorted_stems.items():
        print("{0:20}{1:20}".format(item, amount))



def main():

    file_path = "test_txt.txt"

    s = stemming(file_path)

main()
