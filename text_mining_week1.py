from urllib import request
from nltk import word_tokenize
from bs4 import BeautifulSoup

url = "https://www.bbc.com/future/article/20230116-how-donkeys-changed-the-course-of-human-history"
html = request.urlopen(url).read().decode('utf8')
# print(html[:600])

raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)

