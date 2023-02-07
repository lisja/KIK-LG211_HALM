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

@app.route('/', methods=['GET', 'POST'])
def index():
    file_path = "enwiki-20181001-corpus.100-articles.txt"
    text, documents = readandcut(file_path)
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        bool_or_tfv_or_stems = request.form.get('mode')
        if bool_or_tfv_or_stems == "boolean":
            # search_bool(input_query, bool_or_tfv_or_stems)
            # print_output(hits_list, bool_or_tfv_or_stems)
            pass
        elif bool_or_tfv_or_stems == "tfv":
            # search_tfv(input_query, bool_or_tfv_or_stems)
            # print_output(hits_list, bool_or_tfv_or_stems)
            pass
        elif bool_or_tfv_or_stems == "stems":
            # additional_tokens = find_related_tokens_from_stem(input_query)
            # search_stems(input_query, bool_or_tfv_or_stems, additional_tokens)
            # print_output(hits_list, bool_or_tfv_or_stems)
            pass
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
