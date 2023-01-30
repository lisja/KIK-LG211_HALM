import re

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    text = str(text)

    cuttext = text.split("</article>")
    cuttext = cuttext[:-1]
    return text, cuttext

file_path = "WEEK_2/enwiki-20181001-corpus.100-articles.txt"
text, cuttext = readandcut(file_path)

def word_set(article):
    article = article.lower()
    article = re.sub(r"[^a-z\s]", "", article)
    words = article.split()
    return set(words)

minisets = [word_set(i) for i in cuttext]
mainset = word_set(text)
vectors = []
for article_set in minisets:
    vector = [1 if word in article_set else 0 for word in mainset]
    vectors.append(vector)
print(vectors[1])