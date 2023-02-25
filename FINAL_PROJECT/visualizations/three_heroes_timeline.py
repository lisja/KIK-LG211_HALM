# visualization to show WHEN which characters appear

from urllib.request import urlopen
import collections
from matplotlib import pyplot as plt
import re
# from sklearn.feature_extraction.text import CountVectorizer
from data_processing_file import heroes_dict, x, y 



f = plt.figure(figsize=(50,30))
ax1 = f.add_subplot(111)


# # # # set formatter and locator of ticks for x axis
# # # ax1.xaxis.set_major_formatter(formatter)
# # # tick_spacing = 1825
# # # ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
# # # ax1.xaxis.grid(True, which='major')
# # # ax1.yaxis.grid(True, which='major')

# # # TODO – set red alpha for Naruto / and maybe others
ax1.scatter(x,y, alpha=0.3)

# # set limits of y axis
# # TODO - see if next line necessary
ax1.set_ylim(len(list(set(y)))+1,-1)
    
ax1.set_ylabel('Heroes in order of appearance', fontsize=18)
ax1.set_xlabel('Series Nr', fontsize=18)
# ax1.set_title('Distribution of diaries\' entries over years', fontsize=24)

# # plt.xticks(rotation=90)
plt.show()

