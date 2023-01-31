from sklearn.feature_extraction.text import CountVectorizer
#task 5 done 
import re

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    # print(text[:200])
    text = str(text)

    text = re.sub("</article>", "</article>/n/n", text)

    cuttext = text.split("/n/n")
    # cuttext = cuttext[:-1]
    return text, cuttext

file_path = "enwiki-20181001-corpus.100-articles.txt"
text, documents = readandcut(file_path)
print("SMOTHING", text[:200])
# print("SMOTHING")
# print(len(documents))
# print()
# print(documents[99])
# print(len(cuttext))


cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)
print(sparse_matrix) 

d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(",
     ")": ")"}

"""documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]"""

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def search(input_query):
    print("Searching...\n\n")
    print("Commands 'AND', 'NOT', and 'OR' always upper case!")
    
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'[A-Za-z0-9]+\b')
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_

    print("Query: '" + input_query + "'")
    #task 2 done
    try:
        print("Rewritten:", rewrite_query(input_query))
        print("Matching:", eval(rewrite_query(input_query)))
        hits_matrix = eval(rewrite_query(input_query))
        hits_list = list(hits_matrix.nonzero()[1])
        for i, doc_idx in enumerate(hits_list):
            first_line = documents[doc_idx].splitlines()[1]
            print("Matching doc #{:d} - {:s}".format(i, first_line))
        print()
    except KeyError:
        print("Query not found in the documents.")
    except SyntaxError:
        print("'AND', 'NOT', and 'OR' are commands. Use lowercase, e.g. 'and', 'not', or 'or'")
    print()

def interface():
    print("Welcome to HALM search engine!\n")

    while True:
    
        print("'q'= Quit")
        input_query = input("Input your query: ")

        if input_query == "q":
            break
        else:
            search(input_query)





def main():
    interface()

main()


