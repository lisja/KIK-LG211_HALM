# program to find all the h3 sized headlines from the BBC front page

from bs4 import BeautifulSoup
import requests

url = "https://www.bbc.com"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")


try:
    content_div = soup.find_all("h3", class_="media__title")

    for i in content_div:
        contents = i.get_text("\n").strip()
        print(contents)
        print()

except:
    print("error happened")
