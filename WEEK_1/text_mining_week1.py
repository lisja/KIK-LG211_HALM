from urllib import request
from nltk import word_tokenize
from bs4 import BeautifulSoup
import ssl

import nltk
nltk.download('punkt')
#I had to add this in order to get the program working in the Terminal, not sure why tho... worked well in PyCharm


url = "https://www.bbc.com/future/article/20230116-how-donkeys-changed-the-course-of-human-history"
#I added ssl to fix the error I was getting (urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>)
context = ssl._create_unverified_context()
html = request.urlopen(url, context=context).read().decode('utf8')

url2 = "https://www.bbc.com/"
#I added ssl to fix the error I was getting (urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>)
context2 = ssl._create_unverified_context()
html2 = request.urlopen(url2, context=context2).read().decode('utf8')

raw = BeautifulSoup(html, 'html.parser').get_text()
raw2 = BeautifulSoup(html2, 'html.parser').get_text()

soup = BeautifulSoup(html, 'html.parser')

print("The whole test text tokenized:")
tokens = word_tokenize(raw)
print(tokens)

print()

print("The found titles from the test text:")
for tag in soup.find_all('title'):
    print(tag)

print()


print()

soup2 = BeautifulSoup(html2, 'html.parser')

print("Found h3 sized titles from the BBC front page:")
for tag in soup2.find_all('h3'):
    print(tag)

