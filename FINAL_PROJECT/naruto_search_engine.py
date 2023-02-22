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

    cuttext = re.split(r'\/\/% \d+$', text, 0, re.MULTILINE)
    
    return text, cuttext

def linesplitter_and_cleaner(document):

    # Splits documents (episodes) into a list of speech lines including the timestamp
    doc_lines = re.split(r'^\d+$', document, 0, re.MULTILINE)
    #doc_lines = document.splitlines()

    for line in doc_lines:
        if len(line) < 1:
            doc_lines.remove(line)
    """
    doc_lines_no_timestamps = doc_lines
    
    for line in doc_lines_no_timestamps:
        line = re.sub('00:.*0',  '', line)
    """
    return doc_lines

# 1c default file_path used
file_path = "naruto3.txt"

# 1d executing readandcut() function and saving full 
# string into "text" and split articles into "documents"
text, documents = readandcut(file_path)

def search_bool(input_query, bool_or_tfv): # search the boolean query
    
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'[A-Za-z0-9_À-ÿ\-]+\b', ngram_range=(1, 2))
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_
    
    try:
                
        hits_matrix = eval(rewrite_query(input_query))
        hits_list = list(hits_matrix.nonzero()[1])
        hits=[]

        for i, doc_idx in enumerate(hits_list):

            doc_lines = linesplitter_and_cleaner(documents[doc_idx])
            
            episode_number = doc_idx
            
            timestamp_and_lines_list = []
            
            
            for i in range(1, len(doc_lines)):
                if input_query in doc_lines[i].lower():
                    timestamp = doc_lines[i][:31]
                    line = doc_lines[i][31:]

                    timestamp_and_lines_tuple = (timestamp, line)

                    timestamp_and_lines_list.append(timestamp_and_lines_tuple)

            for timestamp_and_line in timestamp_and_lines_list:
                #episode_line = timestamp_and_line[0] + ":" + timestamp_and_line[1] + "\n"
                hits.append({"article_name":episode_number, "article_score":timestamp_and_line[0], "article_content":timestamp_and_line[1]})

        return hits, len(hits)
        
    except:
        hits=[]
        amount = 0
        article_name = "Error"
        article_content = "Query not found in the documents."
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits, amount

def search_stems(input_query, bool_or_tfv_or_stems, additional_tokens): # search the stems

    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'[A-Za-z0-9_À-ÿ\-]+\b')
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_
    hits=[]

    try:
        # this IF block added for Stemmer functionality
        if type(additional_tokens) is list:
            hits_list = []
            for token in additional_tokens:
                hits_matrix = eval(rewrite_query(token))
                hits_list.append(list(hits_matrix.nonzero()[1]))
            hits_list = list(set([item for items in hits_list for item in items]))
            # print("hits_list from IF: ", hits_list)
        else:
            hits_matrix = eval(rewrite_query(input_query))
            hits_list = list(hits_matrix.nonzero()[1])
            # print("hits_list from ELSE: ", hits_list)

    
        #print("Additional tokens from Stemmer: ", additional_tokens)
        for i, doc_idx in enumerate(hits_list):
            
            doc_lines = linesplitter_and_cleaner(documents[doc_idx])
            episode_number = doc_idx
            first_line = '\n'.join(doc_lines[:5])

            timestamp_and_lines_list = []
            
            # Separate timestamp and line
            for i_line in range(1, len(doc_lines)):
                if input_query in doc_lines[i_line].lower():
                    timestamp = doc_lines[i_line][:31]
                    line = doc_lines[i_line][31:]

                    timestamp_and_lines_tuple = (timestamp, line)

                    timestamp_and_lines_list.append(timestamp_and_lines_tuple)

            for timestamp_and_line in timestamp_and_lines_list:
                hits.append({"article_name":episode_number, "article_score":timestamp_and_line[0], "article_content":timestamp_and_line[1]})

        return hits, len(hits)

    except:
        hits=[]
        article_name = "Error"
        article_content = "Query not found in the documents."
        amount = 0
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits, amount
    

def search_tfv(input_query, bool_or_tfv_or_stems):
    #if input is in quotes, use bigrams only (c. Multi-word phrases)
    try:
        if input_query.startswith('"') and input_query.endswith('"'):
            input_query = input_query[1:-1] # remove the quotes
            try:
                gv = TfidfVectorizer(lowercase=True, ngram_range=(2, 2), sublinear_tf=True, use_idf=True, norm="l2")
            except IndexError:
                gv = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), sublinear_tf=True, use_idf=True, norm="l2")
        else:
            gv = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), sublinear_tf=True, use_idf=True, norm="l2")
    
        g_matrix = gv.fit_transform(documents).T.tocsr()

    # Vectorize query string
        query_vec = gv.transform([ input_query ]).tocsc()

    # Cosine similarity
        hits = np.dot(query_vec, g_matrix)

    # Rank hits
        ranked_scores_and_doc_ids = \
            sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                reverse=True)

        hits=[]

                    
        for i_doc, doc_idx in enumerate(ranked_scores_and_doc_ids):

            score = doc_idx[0] #Unused score number, probably not necessary for user.
            doc_idx = doc_idx[1]
            count = 0

            doc_lines = linesplitter_and_cleaner(documents[doc_idx])
            
            episode_number = doc_idx

            # Separate timestamp and line
            for i_line in range(1, len(doc_lines)):
                if input_query in doc_lines[i_line].lower():
                    timestamp = doc_lines[i_line][:31]
                    line = doc_lines[i_line][31:]

                    # Count number of hits on a speech line
                    count += len(re.findall(input_query, line.lower()))

            # "Best match" for the best one, and then for example "2. best match" for the rest     
            if i_doc == 0:
                best_match = "Best match: Episode " + str(doc_idx)
            elif i_doc > 0:
                best_match = str(i_doc+1) + ". best match: Episode " + str(doc_idx)

            # Make the count into a string plus the "number of hits" string before it
            count_str = "Number of hits: " + str(count)
            
            hits.append({"article_name":episode_number, "article_score":best_match, "article_content":count_str})
      
        return hits, len(hits)

    except:
        hits=[]
        amount = 0
        article_name = "Error"
        article_content = "Query not found in the documents."
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits, amount



d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(",
     ")": ")"}

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # rewrites tokens

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def stemming(file_path): 

    stemmer = PorterStemmer()
    # words = word_tokenize(text[:3000])
    words = word_tokenize(text)

    # loop over all tokens and save one_to_one 'token':'stem' pair in a dict
    token_to_stem_dict = {}
    for i in words:
        if i.lower() not in token_to_stem_dict:
            token_to_stem_dict[i.lower()] = stemmer.stem(i)
    
    # loop over 'token':'stem' pairs in dict and reverse order to 'stem': ['token1', 'token2', 'token3', etc]
    stem_to_tokens_dict = {}    
    for key, value in token_to_stem_dict.items():
        if value not in stem_to_tokens_dict:
            stem_to_tokens_dict[value] = [key]
        else:
            stem_to_tokens_dict[value].append(key)

    # print("stem_to_tokens_dict: ", stem_to_tokens_dict)
    return token_to_stem_dict, stem_to_tokens_dict

token_to_stem_dict, stem_to_tokens_dict = stemming(file_path)

# 3e find_related_tokens_from_stem – and return a list of words for search
def find_related_tokens_from_stem(token):
    try:
        stem = token_to_stem_dict[token]
        list_of_words_to_look_for = stem_to_tokens_dict[stem]
    # print(list_of_words_to_look_for)
        return list_of_words_to_look_for
    except KeyError: # error handling if query not in text
        return [token]

@app.route('/', methods=['GET', 'POST'])
def index():
    file_path = "naruto3.txt"
    text, documents = readandcut(file_path)
    matches = []
    amount = 0
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        bool_or_tfv_or_stems = request.form.get('mode')
        if bool_or_tfv_or_stems == "boolean":
            matches, amount = search_bool(input_query, bool_or_tfv_or_stems)
            
        elif bool_or_tfv_or_stems == "tfv":
             matches, amount = search_tfv(input_query, bool_or_tfv_or_stems)
            
        elif bool_or_tfv_or_stems == "stems":
             additional_tokens = find_related_tokens_from_stem(input_query)
             matches, amount = search_stems(input_query, bool_or_tfv_or_stems, additional_tokens)
            
    amount = len(matches) # the amount of articles found
    return render_template('index.html', results=matches, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
