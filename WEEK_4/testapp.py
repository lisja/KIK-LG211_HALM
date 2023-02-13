from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import *
from nltk.tokenize import sent_tokenize, word_tokenize
import operator
import time
from nltk.stem import PorterStemmer
global documents



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

def search_bool(input_query, bool_or_tfv_or_stems):
    hits_list = []
    for document in documents:
        lines = linesplitter_and_cleaner(document)
        for line in lines:
            if input_query in line:
                hits_list.append(line)
    return hits_list

def search_tfv(input_query, bool_or_tfv_or_stems):
    hits_list = []
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    input_query = [input_query]
    query_matrix = tfidf.transform(input_query)
    cosine_similarities = np.dot(tfidf_matrix.toarray(), query_matrix.T.toarray())
    cosine_similarities = cosine_similarities.flatten()
    sorted_indices = cosine_similarities.argsort()[:-6:-1]
    for index in sorted_indices:
        hits_list.append(documents[index])
    return hits_list

def search_stems(input_query, mode, additional_tokens):
    hits_list = []
    stemmed_query = []
    stemmer = PorterStemmer()
    for word in word_tokenize(input_query):
        stemmed_word = stemmer.stem(word)
        stemmed_query.append(stemmed_word)
    stemmed_query = " ".join(stemmed_query)

    for i, document in enumerate(documents):
        stemmed_lines = linesplitter_and_cleaner(document)
        stemmed_doc = ""
        for line in stemmed_lines:
            stemmed_words = []
            for word in word_tokenize(line):
                stemmed_word = stemmer.stem(word)
                stemmed_words.append(stemmed_word)
            stemmed_line = " ".join(stemmed_words)
            stemmed_doc += stemmed_line

        if re.search(stemmed_query, stemmed_doc):
            hits_list.append(i)

    return hits_list


@app.route('/', methods=['GET', 'POST'])
def index():
    file_path = "enwiki-20181001-corpus.100-articles.txt"
    text, documents = readandcut(file_path)
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        bool_or_tfv_or_stems = request.form.get('mode')
        if bool_or_tfv_or_stems == "boolean":
            hits_list = search_bool(input_query, documents)
            print_output(hits_list, bool_or_tfv_or_stems)
        elif bool_or_tfv_or_stems == "tfv":
            hits_list = search_tfv(input_query, documents)
            print_output(hits_list, bool_or_tfv_or_stems)
        elif bool_or_tfv_or_stems == "stems":
            additional_tokens = find_related_tokens_from_stem(input_query)
            hits_list = search_stems(input_query, documents, additional_tokens)
            print_output(hits_list, bool_or_tfv_or_stems)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
