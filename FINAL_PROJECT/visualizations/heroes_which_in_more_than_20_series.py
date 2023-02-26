#  Heroes who appear in MORE THAN 20 series:
from matplotlib import pyplot as plt
from data_processing_file import large_dict

# filtering for Heroes who appear in MORE THAN 20 series:
sorted_list = [[key, value] for key, value in large_dict.items() if len(value) > 20]

# sorting for visualization by number of appearances:
sorted_list = sorted(sorted_list, key=lambda x: len(x[1]), reverse=True)

# create x,y data_points for every scatter plot circle
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

ax1.xaxis.grid(True, which='major')
# ax1.yaxis.grid(True, which='major')

ax1.scatter(x,y, alpha=0.3)

ax1.set_ylim(len(list(set(y)))+1,-1) 
ax1.set_ylabel('Heroes by most frequent', fontsize=18)
ax1.set_xlabel('Series Nr', fontsize=18)
ax1.set_title('Heroes who appear in MORE THAN 20 series', fontsize=24)

plt.show()

