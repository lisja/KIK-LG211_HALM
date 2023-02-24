from urllib.request import urlopen
import collections
import re
from naruto_frequencies_dict import frequencies_dict

"""
This file contains functionality to tokenize naruto.txt
in different formats needed for visualizations.
The processing results are saved in variables and directly
imported into visualization files.
"""


naruto_txt = "https://raw.githubusercontent.com/lisja/KIK-LG211_HALM/main/WEEK_5/naruto3.txt"
# naruto_txt = "/Users/Haralds/Desktop/H/Helsinki/Helsinki-Courses-2021/building-nlp-applications/KIK-LG211_HALM/WEEK_5/naruto3.txt"

en_stopwords = ["it", "you", "them", "that", "right", "what", "me", "time", 
"this", "oh", "here", "now", "but", "no", "too", "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"] 

heroes_dict = {
  'Kiba': 116, 'Akamaru': 103, 'Yakumo': 66, 'Shino': 63, 'Naruto': 786, 'Unkai': 4, 'Kurenai': 20,  'Hinata': 137, 
  'Sakura': 244, 'Fuki': 2, 'Tsunade': 206, 'Menma': 12, 'Sasuke': 587, 'Lee': 134, 'Asuma': 11, 'Anko': 12, 'Orochimaru': 167, 'Kabuto': 29, 'Ino': 74,  'Neji': 112, 'Kakashi': 77,
  'Tenten': 24, 'Gaara': 123, 'Itachi': 21, 'Kimimaro': 12,  'Mizuki': 50, 'Zabuza': 41, 'Senbon': 3, 'Inari': 26, 'Haku': 22, 'Iruka': 42,  'Konohamaru': 15, 'Moegi': 7, 'Shikamaru': 75, 
  'Todoroki': 13, 'Kurama': 5, 'Yuhi': 5, 'Toki': 5, 'Akatsuki': 11,'Toad': 17, 'Choji': 84, 'Jiraiya': 54, 
  'Jiga': 2, 'Ayame': 14, 'Fuma': 3, 'Sasame': 37, 'Arashi': 21, 'Temari': 22, 'Kankuro': 16, 'Shukaku': 13,'Kunihisa': 1, 'Tokichi': 3, 
  'Sarutobi': 13, 'Ibiki': 8, 'Bikochu': 43, 'Kamizuru': 1, 'Tsunade': 2, 'Hanzaki': 1, 'Hizashi': 3, 'Hiashi': 6, 
  'Kisame': 12, 'Neji': 1, 'Orochimaru': 1, 'Yurinojou': 3, 'Morino': 6, 'Mitarashi': 1, 'Kagetsu': 3, 'Futa': 3, 'Akahoshi': 39, 
  'Hokuto': 6, 'Kagero': 2, 'U-zu-ma-ki': 1, 'Fukusuke': 5, 'Rokusuke': 11, 'Raiga': 28, 'Karashi': 26, 'Ranmaru': 26, 'Wagarashi': 4, 'Onbaa': 10, 
  'Yamanaka': 3, 'Onbu': 1, 'Sansho': 7, 'Kanpachi': 1, 'Degarashi': 2, 'Natsuhi': 7, 'Yagura': 10, 'Gekko': 1, 'Kubisaki': 4, 'Gosa': 1, 
  'Kurosuki': 1, 'Agira': 1, 'Wasabi': 1
}

heroes_list_FINAL = ['Kiba', 'Akamaru', 'Yakumo', 'Shino', 'Naruto', 'Unkai',
'Kurenai', 'Hinata', 'Sakura', 'Fuki', 'Tsunade', 'Menma', 'Sasuke', 'Lee', 'Asuma', 'Anko', 'Orochimaru', 'Kabuto', 
'Ino', 'Neji', 'Kakashi', 'Tenten', 'Gaara', 'Itachi', 'Kimimaro', 'Mizuki', 'Zabuza', 'Senbon', 'Inari', 'Haku', 'Iruka', 'Konohamaru', 
'Moegi', 'Shikamaru', 'Todoroki', 'Kurama', 'Yuhi', 'Toki', 'Akatsuki', 'Toad', 'Choji', 'Jiraiya', 'Jiga', 'Ayame', 'Fuma', 'Sasame', 
'Arashi', 'Temari', 'Kankuro', 'Shukaku', 'Kunihisa', 'Tokichi', 'Sarutobi', 'Ibiki', 'Bikochu', 'Kamizuru', 'Hanzaki', 'Hizashi', 
'Hiashi', 'Kisame', 'Yurinojou', 'Morino', 'Mitarashi', 'Kagetsu', 'Futa', 'Akahoshi', 'Hokuto', 'Kagero', 'U-zu-ma-ki', 'Fukusuke',
'Rokusuke', 'Raiga', 'Karashi', 'Ranmaru', 'Wagarashi', 'Onbaa', 'Yamanaka', 'Onbu', 'Sansho', 'Kanpachi', 'Degarashi', 'Natsuhi',
'Yagura', 'Gekko', 'Kubisaki', 'Gosa', 'Kurosuki', 'Agira', 'Wasabi']

heroes_lowercased = [item.lower() for item in heroes_list_FINAL]
# print("heroes_lowercased: ", heroes_lowercased)



# 1 PROCESSING PART for one_wordcloud file:
def get_frequency_list(data_url):
    try:
        data = urlopen(data_url)
        words = []
        text = data.read().decode(data.headers.get_content_charset())
        
        lines = text.split("\n")
        for line in lines:
            array = line.split(" ")
            array = [item.lower() for item in array]
            words.extend(array)
        
        frequency_list = dict(collections.Counter(words))
        filtered_frequency_list = dict()
        for k,v in frequency_list.items():
            stripped = re.sub("[,\.:;-?!…'’]", "", k)
            if frequency_list.get(stripped, 0) > v and stripped not in en_stopwords and stripped not in heroes_list_FINAL and stripped not in heroes_lowercased:
                filtered_frequency_list[stripped] = filtered_frequency_list.get(stripped, 0) + v

        result = {k:v for k,v in filtered_frequency_list.items() if len(k) > 1}
        print()
        print(" ... naruto.txt accessed for processing from INTERNET")

    except:
        result = frequencies_dict
        print()
        print(" ... processed frequencies_dict accessed from local file, because internet not working")

    return result

# calculated results for the one_wordcloud visualization
DATA = naruto_txt
freqs = get_frequency_list(DATA)



# 2 Data processing for Wordcloud 2 – function to create data 
# for HEROES wordcloud – NOT USED CURRENTLY
def get_frequency_list_second(data_url):

  with open(data_url, "r") as file:
    text = file.read()
    words = []
    lines = text.split("\n")
    for line in lines:
      array = re.split(" |'|’", line)
      for item in array:
        if item.lower() != item:
          words.extend([item])
    
    frequency_list = dict(collections.Counter(words))
    filtered_frequency_list = dict()
    for k,v in frequency_list.items():
      stripped = re.sub("[,\.:;-?!…]", "", k)
      if frequency_list.get(stripped, 0) > v and stripped in heroes_dict:
        filtered_frequency_list[stripped] = filtered_frequency_list.get(stripped, 0) + v

    return {k:v for k,v in filtered_frequency_list.items() if len(k) > 1}