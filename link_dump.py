import re
import urllib
import json
from robobrowser import RoboBrowser
from time import sleep


SEARCH_TERM="linux usb device debug"

google_site="https://www.google.com/search?q={0}&ie=utf-8&oe=utf-8{1}"
USSR = "Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0"


def google_urls(term, pages=2):
    """Get urls from google. Returns list of urls."""
    t = urllib.quote(term)
    browser = RoboBrowser(user_agent=USSR)
    
    fresults = []
    for i in range(pages):
        off = '&start={0}'.format(i*10)
        browser.open(google_site.format(t, off))
        term = lambda x: x.findChild('a').attrs['href']
        results = browser.find_all('h3', {"class": "r"})
        results = map(term, results)
        fresults.extend(results)
        sleep(0.1)

    return results
        

def main():
    print json.dumps(google_urls(SEARCH_TERM))


if __name__ == '__main__':
    main()
