"""from sklearn.feature_extraction.text import CountVectorizer



def count_and_sparse():
    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform(documents)

    print("Term-document matrix: (?)\n")
    print(sparse_matrix)
"""

def search(input_query):
    print("Searching...\n\n")

def interface():
    print("Welcome to HALM search engine!\n")

    while True:
    
        print("'q'= Quit")
        input_query = input("Input your query: ")

        if input_query == "q":
            break
        else:
            search(input_query)

import re

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

   
    text = str(text)

    
    cuttext = re.split(r"<", text)
    cuttext.pop(0)
    return cuttext


file_path = "/GitHub/KIK-LG211_HALM/WEEK_2/enwiki-20181001-corpus.100-articles.txt"
cuttext = readandcut(file_path)

print(cuttext[0])

            

def main():
    interface()

main()
    
    
    


