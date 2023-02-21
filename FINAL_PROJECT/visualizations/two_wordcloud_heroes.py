# visualization to show WHEN which characters appear

from urllib.request import urlopen
import collections
from matplotlib import pyplot as plt
import re
import wordcloud


# naruto_txt = "https://raw.githubusercontent.com/lisja/KIK-LG211_HALM/main/WEEK_5/naruto3.txt"
naruto_txt = "/Users/Haralds/Desktop/H/Helsinki/Helsinki-Courses-2021/building-nlp-applications/KIK-LG211_HALM/WEEK_5/naruto3.txt"

heroes = {
  'Kiba': 116, 'Genjutsu': 73, 'Akamaru': 103, 
  'Sensei': 211, 'Hokage': 278, 'Yakumo': 66, 'Shino': 63,
  'Naruto': 786, 'Unkai': 4, 'Kurenai': 20, 'Shinobi': 126, 
  'Hinata': 137, 'Sakura': 244, 'Fuki': 2, 'Grandma': 15, 
  'Tsunade': 206, 'Uzumaki': 28, 'Menma': 12, 'Sasuke': 587,  
  'Chakra': 231, 'Lee': 134, 'Taijutsu': 34, 'Genkai': 23, 
  'Asuma': 11, 'Isaribi': 11,  'Anko': 12, 'Orochimaru': 167, 
  'Jutsu': 310, 'Kabuto': 29, 'Chakras': 4, 'Genin': 30,
  'Ino': 74, 'Ninja': 247, 'Komei': 17, 'Warrior': 28, 'Moso': 15, 'Neji': 112, 'Kakashi': 77,
  'Pakkun': 2, 'Clone': 30, 'Sagi': 41, 'Tenten': 24, 
  'Ninjutsu': 47, 'Sharingan': 74, 'Gaara': 123, 
  'Chishima': 14, 'Owashi': 5, 'Uchiha': 69,  'Itachi': 21, 
  'Mother': 21, 'Brother': 123, 'Byakugan': 28, 'Kimimaro': 12, 
  'Mark': 13, 'Fang': 37, 'Gosunkugi': 20, 'Master': 6, 
  'Jonin': 14, 'Shuriken': 18, 'Darn': 85, 'Fox': 15, 'Mizuki': 50, 
  'Zabuza': 41, 'Senbon': 3, 'Inari': 26, 'Grandpa': 4, 
  'Haku': 22, 'Yoroi': 3, 'Hyuga': 27, 'Zaku': 3, 
  'Tazuna': 19, 'Potchi': 1, 'Kaiza': 4,  'Dad': 4, 
  'Iruka': 42,  'Konohamaru': 15, 'Moegi': 7, 'Shikamaru': 75, 
  'Shisui': 5, 'Shrine': 11, 'Akio': 12, 'Gantetsu': 39, 
  'Todoroki': 13, 'Kurama': 5, 'Yuhi': 5, 'Toki': 5, 
  'Akatsuki': 11,'Toad': 17, 'Choji': 84, 
  'Genno': 13, 'Chunin': 34, 'Ichiraku': 10,'Gennin': 1, 
  'Rasengan': 6, 'Chidori': 11,'Shiin': 1, 'Sage': 57, 
  'Jiraiya': 54, 'Sannin': 28, 'Kikunojou': 9, 'Kikusuke': 4, 'Haruna': 9, 
  'Janin': 3, 'Ebisu': 5, 'Boss': 29,  'Grandson': 3, 
  'Haruno': 7, 'Inuzuka': 7, 'Aburame': 9, 
  'Nara': 6, 'Akimichi': 5, 'Shinobi"': 2, 
  'Jiga': 2, 'Ayame': 14, 'Fuma': 3, 'Sasame': 37, 'Arashi': 21, 
  'Wolf': 2, 'Temari': 22, 'Kankuro': 16, 
  'Shukaku': 13,'Kunihisa': 1, 'Tokichi': 3, 
  'Strange': 1, 'Proctor': 5,'Agari': 1, 'Kidomaru': 1, 
  'Jirobo': 4, 'Kujaku': 11, 'Fujin': 3,  'Shizune': 1, 'McCoy': 1,
  'Sarutobi': 13, 'Ibiki': 8, 'Anbu': 10, 
  'Bikochu': 43, 'Kamizuru': 1, 'Raijin': 2, 
  'Tsunade': 2, 'Hanzaki': 1, 'Hizashi': 3, 'Hiashi': 6, 
  'Fuuma': 1, 'Kunoichi': 6, 'Kisame': 12,  'Hokage': 1,
  'Neji': 1, 'Dosu': 4, 'Hayate': 3,'Akagi': 3, 'Jirocho': 7, 
  'Kazekage': 5,'Kunai': 1,'Senbons': 3, 'Aoi': 4, 'Idate': 28, 'Orochimaru': 1, 
  'Mizura': 16, 'Sumaru': 42, 'Hoshikage': 15,'Dojo': 11, 
  'Yurinojou': 3, 'Morino': 6, 'Mitarashi': 1, 'Gatô': 2,  
  'Kagetsu': 3, 'Futa': 3, 'Akahoshi': 39, 'Hokuto': 6, 
  'Kagero': 2, 'U-zu-ma-ki': 1, 'Fukusuke': 5,  'Rokusuke': 11, 'Raiga': 28, 'Karashi': 26, 'Ranmaru': 26,
  'Wagarashi': 4, 'Onbaa': 10, 'Yamanaka': 3, 'Onbu': 1, 
  'Sansho': 7, 'Kanpachi': 1, 'Degarashi': 2, 'Natsuhi': 7, 
  'Yagura': 10, 'Gekko': 1, 'Kubisaki': 4, 'Gosa': 1, 'Kurosuki': 1, 
  'Agira': 1, 'Wasabi': 1
}

def get_frequency_list(data_url):

  with open(data_url, "r") as file:
    text = file.read()

    words = []
    lines = text.split("\n")
    for line in lines:
      # TODO – add line to include only lines starting with non-digit
      # if not line[0].isdigit():
      # array = line.split(" ")
      array = re.split(" |'|’", line)
      # print(array)
      # print(type(array))
      for item in array:
        if item.lower() != item:
          words.extend([item])
      # array = [item for item in array if item[0] == item.upper()[0]]
      # array = [item for item in array if item[0] == item.upper()[0]]
      # words.extend(array)
      # words.extend(line.split(" "))
    
    frequency_list = dict(collections.Counter(words))
    filtered_frequency_list = dict()
    for k,v in frequency_list.items():
      stripped = re.sub("[,\.:;-?!…]", "", k)
      if frequency_list.get(stripped, 0) > v and stripped in heroes:
        filtered_frequency_list[stripped] = filtered_frequency_list.get(stripped, 0) + v

  # TODO – add line to check IF word not in STOPWORDS list, and then only include
  # TODO – stopwords list need to be created

    return {k:v for k,v in filtered_frequency_list.items() if len(k) > 1}


DATA = naruto_txt
freqs = get_frequency_list(DATA)
print("freqs: ", freqs)

wcloud = wordcloud.WordCloud().generate_from_frequencies(freqs)
plt.imshow(wcloud)
plt.show()