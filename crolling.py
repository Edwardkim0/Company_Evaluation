import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://www.amazon.com/books-used-books-textbooks/b?ie=UTF8&node=283155")
# html = urlopen("https://biz.chosun.com/")
bsObject = BeautifulSoup(html, "html.parser")
print(bsObject.prettify())
for meta in bsObject.head.find_all('meta',{"name":"description"}):
    print(meta.get('content'))

for object in bsObject:
    print(object.keys)