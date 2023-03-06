"""
1st Visualization – shows a Wordcloud of most 
frequent words when removed [1] stopwords and [2] Heroes.
"""

from matplotlib import pyplot as plt
import wordcloud
from data_processing_file import freqs

wcloud = wordcloud.WordCloud(width=500, height=400).generate_from_frequencies(freqs)
# plt.imshow(wcloud)
plt.imshow(wcloud, aspect="equal")
# next line - to remove axis, ticks and numbers around wordcloud
plt.axis("off")
plt.savefig('one_wordcloud_non_heroes.png', figsize=(15,5), dpi=100)
plt.show()