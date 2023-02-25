# visualization to show WHEN which characters appear

from matplotlib import pyplot as plt
import numpy as np
from data_processing_file import bar_x1, bar_x2, bar_y

f = plt.figure(figsize=(50,30))
ax1 = f.add_subplot(111)

bar_size = 0.3
padding = 0.25
y_locs = np.arange(len(bar_y))

ax1.barh(y_locs, bar_x1, height=bar_size, alpha=0.7, label='total mentions of a hero')
ax1.barh(y_locs + bar_size, bar_x2, height=bar_size, color="r", alpha=0.7, label='in how many series present out of 219')

ax1.set(yticks=y_locs, yticklabels=bar_y)
ax1.set_ylim(len(list(set(bar_y)))+1,-1)
ax1.set_ylabel('Heroes by most frequent in appearances', fontsize=18, rotation = 270)
ax1.yaxis.set_label_coords(-0.125, 0.5)
ax1.set_xlabel('Count', fontsize=18)
ax1.set_title('Heroes appearance in total and in unique series', fontsize=24)

ax1.xaxis.grid(True, which='major')
ax1.yaxis.grid(True, which='major')

ax1.legend(fontsize=16)
plt.show()

