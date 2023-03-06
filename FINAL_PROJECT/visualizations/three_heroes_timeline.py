# visualization to show WHEN which characters appear on timeline
from matplotlib import pyplot as plt
from data_processing_file import sorted_list

# create x,y data_points for every data_point
x_values = []
y_values = []
for my_list in sorted_list:
  # print(my_list)
  for el in my_list[1]:
    x_values.append(el)
    y_values.append(my_list[0])
y = y_values
x = x_values

f = plt.figure(figsize=(50,30))
ax1 = f.add_subplot(111)

# # # # set formatter and locator of ticks for x axis
# # # ax1.xaxis.set_major_formatter(formatter)
# # # tick_spacing = 1825
# # # ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax1.xaxis.grid(True, which='major')
ax1.yaxis.grid(True, which='major')

ax1.scatter(x,y, alpha=0.3)

ax1.set_ylim(len(list(set(y)))+1,-1) 
ax1.set_ylabel('Heroes in order of appearance', fontsize=18)
ax1.set_xlabel('Series Nr', fontsize=18)
ax1.set_title('All 89 Heroes on timeline of 219 Series', fontsize=24)

# # plt.xticks(rotation=90)
plt.savefig('three_heroes_on_timeline.png', figsize=(5,4), dpi=50)
plt.show()

