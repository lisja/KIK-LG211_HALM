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

    cuttext = text.split("//%")
    cuttext = cuttext[:-1]
    return text, cuttext

def linesplitter_and_cleaner(document):
    doc_lines = document.splitlines()
    for line in doc_lines:
        if len(line) < 1:
            doc_lines.remove(line)
    return doc_lines

# 1c default file_path used
file_path = "naruto3.txt"

# 1d executing readandcut() function and saving full 
# string into "text" and split articles into "documents"
text, documents = readandcut(file_path)

def print_output(hits_list, bool_or_tfv_or_stems):
        pass
        """
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
        """        
        #return render_template("index.html")
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
        #print_output(hits_list, bool_or_tfv)
        hits=[]
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
                hits.append({"article_name":article_name, "article_content":first_line[:100]})


        print()
    except KeyError:
        return "Query not found in the documents."
    except SyntaxError:
        return "AND', 'AND NOT', and 'OR' are commands. Use lowercase, e.g. 'and', 'not', or 'or'"
    print()

    #In case of an error, returns error:
    try:
        return hits
    except:
        hits=[]
        article_name = "Error"
        article_content = "Error"
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits

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

                #tfv gives tuples, so to make the code work, it has to be split into score and the index
                if type(doc_idx) == tuple:
                        score = doc_idx[0]
                        doc_idx = doc_idx[1]

                doc_lines = linesplitter_and_cleaner(documents[doc_idx])
                article_name = doc_lines[0]
                first_line = '\n'.join(doc_lines[:5])

                #Deletes the article name tag from the article_name
                #article_name = re.sub(r'<article name="(.*?)">', r'\1', article_name)
                hits.append({"article_name":article_name, "article_content":first_line[:100]})          


        return hits
    except:
        hits=[]
        article_name = "Error"
        article_content = "Error"
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits
    

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
        
        for i, doc_idx in enumerate(ranked_scores_and_doc_ids):

                #tfv gives tuples, so to make the code work, it has to be split into score and the index
                if type(doc_idx) == tuple:
                        score = doc_idx[0]
                        doc_idx = doc_idx[1]

                doc_lines = linesplitter_and_cleaner(documents[doc_idx])
                article_name = doc_lines[0]
                first_line = doc_lines[1]
                rating = "Rating: " + str(score)

                #Deletes the article name tag from the article_name
                article_name = re.sub(r'<article name="(.*?)">', r'\1', article_name)
                hits.append({"article_name":article_name, "article_score":rating, "article_content":first_line[:100]})
                
        try:
            return hits
        except:
            hits=[]
            article_name = "Error"
            article_content = "Error"
            hits.append({"article_name":article_name, "article_content":article_content})
            return hits
    except:
        hits=[]
        article_name = "Error"
        article_content = "Error"
        hits.append({"article_name":article_name, "article_content":article_content})
        return hits



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
    file_path = "enwiki-20181001-corpus.100-articles.txt"
    text, documents = readandcut(file_path)
    matches = []
    if request.method == 'POST':
        input_query = request.form.get('input_query')
        bool_or_tfv_or_stems = request.form.get('mode')
        if bool_or_tfv_or_stems == "boolean":
            matches = search_bool(input_query, bool_or_tfv_or_stems)
            #print_output(hits_list, bool_or_tfv_or_stems)
            
        elif bool_or_tfv_or_stems == "tfv":
             matches = search_tfv(input_query, bool_or_tfv_or_stems)
            # print_output(hits_list, bool_or_tfv_or_stems)
            
        elif bool_or_tfv_or_stems == "stems":
             additional_tokens = find_related_tokens_from_stem(input_query)
             #matches = search_stems(input_query, bool_or_tfv_or_stems, additional_tokens)
             matches = search_stems(input_query, bool_or_tfv_or_stems, additional_tokens)
            # print_output(hits_list, bool_or_tfv_or_stems)
            
    amount = len(matches) # the amount of articles found
    return render_template('index.html', results=matches, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
