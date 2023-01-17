from urllib import request

# >>> response = request.urlopen(url)
# >>> raw = response.read().decode('utf8')

url = "https://www.bbc.com/future/article/20230116-how-donkeys-changed-the-course-of-human-history"
html = request.urlopen(url).read().decode('utf8')
print(html[:600])