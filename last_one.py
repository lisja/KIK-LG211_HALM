from bs4 import BeautifulSoup
import requests  # using another package than in the 1st example

url = "https://bbc.com/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")  
# print(soup)

# here I opened html file in Web console and copied the html selector 
# of the class_ to target only text inside
try:
    content_div = soup.find("div", class_="data-bbc-title")
    # print(content_div)
    contents = content_div.get_text("\n")
    print(contents)

except:
    print("error happened")
