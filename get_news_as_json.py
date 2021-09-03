import json
import requests

from datetime import datetime
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

articleLinks = set()
dataAll = []

def getArticleLinks(tag, page):
    
    url = f'https://www.trtworld.com/{tag}?page={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')   
    articleLinks = {'https://www.trtworld.com' + a['href'] for a in soup.find_all('a', {'class': 'gtm-topic-latest-article'})}

    for articleLink in articleLinks:
        r = requests.get(articleLink, headers=headers)
        item = BeautifulSoup(r.text, 'html.parser')
        content = item.find("div", {"class":"contentBox bg-w noMedia"})
        if content:
            content = content.findAll('p')
            data = {'tag': tag,
                    'datetime': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),  
                    'title': item.find('h1', {'class': 'article-title'}).text,
                    'website': 'trtworld',
                    'link': url,
                    'article': [p.text for p in content]}
            print(data)
            dataAll.append(data)
    return
      
if __name__ == '__main__':

    getArticleLinks('art-culture', 15)
          
    with open('/data/articles_'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.json', 'w') as outfile:
        json.dump(dataAll, outfile)
          
