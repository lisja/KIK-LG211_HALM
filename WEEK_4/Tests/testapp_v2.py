from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import *
from nltk.tokenize import sent_tokenize, word_tokenize
import operator
import time

app = Flask(__name__)

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    text = str(text)

    cuttext = text.split("</article>")
    cuttext = cuttext[:-1]
    return text, cuttext

def linesplitter_and_cleaner(document):
    doc_lines = document.splitlines()
    for line in doc_lines:
        if len(line) < 1:
            doc_lines.remove(line)
    return doc_lines

# 1c default file_path used
file_path = "enwiki-20181001-corpus.100-articles.txt"

# 1d executing readandcut() function and saving full 
# string into "text" and split articles into "documents"
text, documents = readandcut(file_path)

def print_output(hits_list, bool_or_tfv_or_stems):
        print("\nThere are/is ", len(hits_list), " hit(s).\n")

        print("-"*30)
        for i, doc_idx in enumerate(hits_list):

                #tfv gives tuples, so to make the code work, it has to be split into score and the index
                if type(doc_idx) == tuple:
                        score = doc_idx[0]
                        doc_idx = doc_idx[1]

                doc_lines = linesplitter_and_cleaner(documents[doc_idx])
                article_name = doc_lines[0]
                first_line = doc_lines[1]

                #Deletes the article name tag from the article_name
                article_name = re.sub(r'<article name="(.*?)">', r'\1', article_name)

                if bool_or_tfv_or_stems == "tfv":
                    print("Article: {:s}\nScore: {:f}\nContent: {:s}...".format(article_name, score, first_line[:100]))
                elif bool_or_tfv_or_stems == "boolean":

                    boolean_return = "Article: {:s}\nContent: {:s}...".format(article_name, first_line[:100])
                    print(boolean_return)
                elif bool_or_tfv_or_stems == "stems":
                    print("Article: {:s}\nContent: {:s}...".format(article_name, first_line[:100]))
                print("-"*30)
        return render_template("index.html")
"""
                #Ask if print 10 more or stop printing
                if i % 10 == 0 and i > 1:
                        stop_or_continue = input("\nWould you like more results (Y / N)? ")
                        if stop_or_continue == "N" or stop_or_continue == "n":
                                break
"""
def search_bool(input_query, bool_or_tfv): # search the query
 #token_pattern=r'[A-Za-z0-9_À-ÿ\-]+\b',
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'[A-Za-z0-9_À-ÿ\-]+\b', ngram_range=(1, 2))
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_

    try:
        
        hits_matrix = eval(rewrite_query(input_query))
        hits_list = list(hits_matrix.nonzero()[1])
        print_output(hits_list, bool_or_tfv)
        
        print()
    except KeyError:
        print("Query not found in the documents.")
    except SyntaxError:
        print("'AND', 'AND NOT', and 'OR' are commands. Use lowercase, e.g. 'and', 'not', or 'or'")
    print()

d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(",
     ")": ")"}

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # rewrites tokens

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

@app.route('/', methods=['GET', 'POST'])
def index():
    file_path = "enwiki-20181001-corpus.100-articles.txt"
    text, documents = readandcut(file_path)
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        bool_or_tfv_or_stems = request.form.get('mode')
        if bool_or_tfv_or_stems == "boolean":
            search_bool(input_query, bool_or_tfv_or_stems)
            #print_output(hits_list, bool_or_tfv_or_stems)
            
        elif bool_or_tfv_or_stems == "tfv":
            # search_tfv(input_query, bool_or_tfv_or_stems)
            # print_output(hits_list, bool_or_tfv_or_stems)
            pass
        elif bool_or_tfv_or_stems == "stems":
            # additional_tokens = find_related_tokens_from_stem(input_query)
            # search_stems(input_query, bool_or_tfv_or_stems, additional_tokens)
            # print_output(hits_list, bool_or_tfv_or_stems)
            pass
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

