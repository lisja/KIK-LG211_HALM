import requests
from bs4 import BeautifulSoup

url1 = "https://yle.fi/a/74-20014091"
url2 = "https://www.bbc.com/travel/article/20230122-the-spanish-town-powered-by-waves"
url3 = "https://edition.cnn.com/2023/01/22/business/ruja-ignatova-cryptoqueen-fbi-most-wanted-cec/index.html"

#get website
page = requests.get(url1)

#parse the content
soup = BeautifulSoup(page.content, "html.parser")

try:

    #find and print title
    print("TITLE:\n")
    title = soup.find_all("h1")[0].text
    print(title)

    #find and print content
    print("\n\nPARAGRAPHS:\n")
    content = soup.find_all("p")
    for i in content:
        print(i.text)
        print()

except:
    print("Error")
