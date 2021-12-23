import urllib.request
from bs4 import BeautifulSoup


def trim_slash(link):
    """trim forward slash from links for constancy"""
    if link[-1] == '/':
        return link[0:-1]
    else:
        return link


def get_links(website):
    """scrape website for links, throws HTTPError if the website is not accessible"""
    req = urllib.request.Request(website, headers={'User-Agent': "Magic Browser"})
    content = urllib.request.urlopen(req)
    soup = BeautifulSoup(content, "html.parser", from_encoding=content.info().get_param('charset'))
    return soup.find_all('a', href=True)
