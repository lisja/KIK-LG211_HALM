"""
2nd Visualization – shows most frequent Heroes
in a Wordcloud.
"""

from matplotlib import pyplot as plt
import wordcloud
from data_processing_file import heroes_dict


wcloud = wordcloud.WordCloud().generate_from_frequencies(heroes_dict)
plt.imshow(wcloud)
plt.show()