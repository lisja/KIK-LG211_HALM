from urllib import request
from nltk import word_tokenize
from bs4 import BeautifulSoup
import ssl

url = "https://www.bbc.com/future/article/20230116-how-donkeys-changed-the-course-of-human-history"
#I added ssl to fix the error I was getting (urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>)
context = ssl._create_unverified_context()
html = request.urlopen(url, context=context).read().decode('utf8')

raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)
