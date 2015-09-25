from functools import partial
from nltk import word_tokenize, tokenize
from pprint import pprint
import operator
import json
import random


def count_occurances(text, occ = None):
    text = text.encode('ascii', 'ignore')
    tokenized_text = word_tokenize(text)
    tokenized_text = [t.upper() for t in tokenized_text]
    map(occ.feed, tokenized_text)

class Occurance(object):
    def __init__(self):
        self._occ = {}

    def feed(self, word):
        try:
            self._occ[word] += 1
        except KeyError:
            self._occ[word] = 1

    def get_occurances(self):
        return self._occ

class TitleGenerator(object):
    like_acc = 100
    tries = 50

    def __init__(self, words, title_limit=10):
        self._words = words
        self._k = self._words.keys()
        self._title_limit = title_limit
        self._rejects = []
    
    def shuffle_choose(self):
        tr = self.tries
        while (tr > 0):
            choice = random.choice(self._k)
            if (self._words[choice] > 0):
                return choice
            tr -= 1
        return choice

    def shuffle_generate_title(self):
        title_len = random.randint(1, self._title_limit)
        title = [self.shuffle_choose() for i in xrange(title_len)]
        return title

    def reject_title(self, title):
        if title not in self._rejects:
            self._rejects.append(title)

    def like_word(self, word):
        self._words[word] += self.like_acc

    def unlike_word(self, word):
        self._words[word] -= self.like_acc


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def like_words(title):
    result = []
    for word in title:
        print "like word[1] or not[0] :", word
        res = getch()
        if res == '1':
            result.append(word)
    return result


with open('texts') as data_file:
    texts = json.load(data_file)


print "text count:", len(texts)

occ = Occurance()
c_count_occurances = partial(count_occurances, occ=occ)
map(c_count_occurances, texts)
t = TitleGenerator(occ.get_occurances())
while True:
    title = t.shuffle_generate_title()
    print title
    print "Is it ok[1] or not[0]:"
    user = getch()
    if user == '1':
        print 'yay!'
        break
    else:
        print 'rejected!'
        t.reject_title(title)
    likes = like_words(title)
    map(t.like_word, likes)
    def un_like(x):
        return t.unlike_word(x) if x not in likes else None
    map(un_like, title)

with open('frequencies.txt', 'w') as f:
    results = sorted(occ.get_occurances().items(),
                     key=operator.itemgetter(1))
    results.reverse()
    f.write(json.dumps(results))

print 'done!'
