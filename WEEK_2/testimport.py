import re

def readandcut(file_path):
    with open(file_path, "r") as file:
        text = file.read()

   
    text = str(text)

    
    cuttext = re.split(r"<", text)
    cuttext.pop(0)
    return cuttext


file_path = "/Users/mike/Documents/GitHub/KIK-LG211_HALM/WEEK_2/enwiki-20181001-corpus.100-articles.txt"
cuttext = readandcut(file_path)

print(cuttext[0])
