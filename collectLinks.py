from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

allExtLinks = set()
allIntLinks = set()

def getInternalLinks(bs, includeUrl):
  try:
      includeUrl = f'{urlparse(includeUrl).scheme}://{urlparse(includeUrl).netloc}'
      internalLinks = []

      for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
          if link.attrs['href'] not in internalLinks:
            if(link.attrs['href']).startswith('/'):
              internalLinks.append(includeUrl+link.attrs['href'])
            else:
              internalLinks.append(link.attrs['href'])
      return internalLinks
  except AttributeError:
    print('Error on capture Internal Link')
    return internalLinks

def getExternalLinks(bs, excludeUrl):
  try:
    externalLinks = []

    for link in bs.find_all('a', href=re.compile('^(http|https|www)((?!'+excludeUrl+').)*$')):
      if link.attrs['href'] is not None:
        if link.attrs['href'] not in externalLinks:
          externalLinks.append(link.attrs['href'])
    return externalLinks
  except AttributeError:
    print('Error on capture External Link')
    return externalLinks

def getAllExternalLinks(siteUrl):
  html = urlopen(siteUrl)
  domain = f'{urlparse(siteUrl).scheme}://{urlparse(siteUrl).netloc}'
  bs = BeautifulSoup(html,'html.parser')

  try:
    externalLinks = getExternalLinks(bs, urlparse(domain).netloc)
    
    for link in externalLinks:
      if link not in allExtLinks:
        allExtLinks.add(link)
        print(f'Link External Added - {link}')  
  except AttributeError:
    print('Error on adding Link External in database.')

  try:
    internalLinks = getInternalLinks(bs,domain)
    
    for link in internalLinks:
      if link not in allIntLinks:
        allIntLinks.add(link)
        print(f'Link Internal Added - {link}')
        getAllExternalLinks(link)
  except AttributeError:
    print('Error on adding Link Internal in database.')

allIntLinks.add('https://www.otempo.com.br/')
getAllExternalLinks('https://www.otempo.com.br/')
