#!/usr/bin/env python3
import re
import sys

import bs4
import requests


class lazy_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Filler(object):
    def __init__(self, github_user='the0demiurge'):
        self.github_user = github_user
        self.cache = dict()

    def get(self, url):
        if url not in self.cache:
            self.cache[url] = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
        return self.cache[url]

    @lazy_property
    def github_followers(self):
        link = f'https://github.com/{self.github_user}'
        soup = self.get(link)
        a_tag = soup.find('a', {'href': f'{link}?tab=followers'})
        return a_tag.find('span').text

    def github_star(self, user, proj):
        url = f"https://github.com/{user}/{proj}"
        soup = self.get(url)
        btn = soup.find_all('a', {'class': 'btn'})
        return btn[2].find_all('span')[-1].text

    def github_fork(self, user, proj):
        url = f"https://github.com/{user}/{proj}"
        soup = self.get(url)
        btn = soup.find_all('a', {'class': 'btn'})
        return btn[1].find_all('span')[-1].text

    def fill(self, data, info, strict=True):
        info = info.copy()
        keys = re.findall(r'(?<=\{)[^\}]+(?=\})', data)
        for k in keys:
            if k not in info:
                if ',' in k:
                    func, *args = k.split(',')
                    if hasattr(self, func):
                        info[k] = getattr(self, func)(*args)
                    elif strict:
                        raise KeyError(k)
                    else:
                        info[k] = k.upper()
                elif hasattr(self, k):
                    info[k] = getattr(self, k)
                elif strict:
                    raise KeyError(k)
                else:
                    info[k] = k.upper()
        return data.format(**info)


if __name__ == '__main__':
    data = ''.join(open(sys.argv[1]).readlines())
    info = {
        'name': 'not telling',
        'email': 'mail',
        'school1': 'sch1',
        'school2': 'scho2',
        'company1': 'comp1',
        'company2': 'comp2',
        'company23': 'c23',
    }

    filler = Filler()

    fmted = filler.fill(data, info, strict=('--test' not in sys.argv))

    print(fmted)
