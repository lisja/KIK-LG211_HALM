import re

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    text = str(text)

    cuttext = text.split("</article>")
    cuttext = cuttext[:-1]
    return text, cuttext

file_path = "enwiki-20181001-corpus.100-articles.txt"
# file_path = "/Users/Haralds/Desktop/H/Helsinki/Helsinki-Courses-2021/building-nlp-applications/KIK-LG211_HALM/WEEK_2/enwiki-20181001-corpus.100-articles.txt"
# file_path = "https://raw.githubusercontent.com/lisja/KIK-LG211_HALM/main/WEEK_2/enwiki-20181001-corpus.100-articles.txt"


text, cuttext = readandcut(file_path)

def word_set(article):
    article = article.lower()
    article = re.sub(r"[^a-z\s]", "", article)
    words = article.split()
    print(set(words))
    return set(words)

minisets = [word_set(i) for i in cuttext]
mainset = word_set(text)
vectors = []
for article_set in minisets:
    vector = [1 if word in article_set else 0 for word in mainset]
    vectors.append(vector)
# print(vectors[1])