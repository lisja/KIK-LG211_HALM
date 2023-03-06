"""
2nd Visualization – shows most frequent Heroes
in a Wordcloud.
"""

from matplotlib import pyplot as plt
import wordcloud
from data_processing_file import heroes_dict

wcloud = wordcloud.WordCloud(width=500, height=400).generate_from_frequencies(heroes_dict)
# plt.imshow(wcloud)
plt.imshow(wcloud, aspect="equal")
# next line - to remove axis, ticks and numbers around wordcloud
plt.axis("off")
plt.savefig('two_wordcloud_heroes.png', figsize=(15,5), dpi=100)
plt.show()