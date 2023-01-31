from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def welcome():

    welcome_message = "Welcome to HALM search engine!"

    print()
    print("*"*len(welcome_message))
    print(welcome_message)
    print("*"*len(welcome_message))
    print()

def choose_bool_or_tfv():

    answer = ""

    while True:
        answer = input("Choose 'boolean' or 'tfv' search: ")
        if answer == "boolean" or answer == "tfv":
            print()
            return answer

def linesplitter_and_cleaner(document):

    #making a list of lines of the document

    doc_lines = document.splitlines()

    #removing lines that are empty

    for line in doc_lines:
        if len(line) < 1:
            doc_lines.remove(line)

    return doc_lines

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    text = str(text)

    cuttext = text.split("</article>")
    cuttext = cuttext[:-1]
    return text, cuttext

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # rewrites tokens

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def search_bool(input_query): # search the boolean query
 
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'[A-Za-z0-9_À-ÿ\-]+\b')
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_

    try:
        
        hits_matrix = eval(rewrite_query(input_query))
        hits_list = list(hits_matrix.nonzero()[1])

        print("\nThere are/is ", len(hits_list), " hit(s).\n")
        print("-"*30, end="\n\n\n")

        
        for i, doc_idx in enumerate(hits_list):
            
            doc_lines = linesplitter_and_cleaner(documents[doc_idx])

            article_name = doc_lines[0]
            first_line = doc_lines[1]

            #Delete the article name tag from the article_name
            article_name = re.sub(r'<article name="(.*?)">', r'\1', article_name)
            
            print("Article: {:s}\n\nContent: {:s}\n\n".format(article_name, first_line))
            print("-"*30)
            
            
        print()
    except KeyError:
        print("Query not found in the documents.")
    except SyntaxError:
        print("'AND', 'NOT', and 'OR' are commands. Use lowercase, e.g. 'and', 'not', or 'or'")
    print()

def search_tfv(input_query):
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=False, use_idf=False, norm=None)
    tf_matrix1 = tfv.fit_transform(documents).T.todense()

def interface(bool_or_tfv):
    
    while True:
    
        print("'q' = Quit; use only lower-case unless using the AND, OR and NOT commands.")
        input_query = input("Input your query: ")

        if input_query == "q":

            quit_message = "Quitting program. Thank you for using the HALM Search Engine!"
            
            print()
            print("*"*len(quit_message))
            print(quit_message)
            print("*"*len(quit_message))
            print()
            
            break
        elif bool_or_tfv == "boolean":
            search_bool(input_query)
        elif bool_or_tfv == "tfv":
            search_tfv(input_query)

def main():
    welcome()
    bool_or_tfv = choose_bool_or_tfv()
    interface(bool_or_tfv)

file_path = "enwiki-20181001-corpus.100-articles.txt"
text, documents = readandcut(file_path)


d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(",
     ")": ")"}


main()


