#!/usr/bin/env python3
import argparse
import json
import os
import re
from copy import deepcopy

import bs4
import requests


class CVFiller(object):
    def __init__(self):
        self.cache = dict()

    def get(self, url):
        if url not in self.cache:
            self.cache[url] = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
        return self.cache[url]

    def github_followers(self, github_user='the0demiurge'):
        link = f'https://github.com/{github_user}'
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

    def fill(self, data, info=None, strict=True):
        if info is None:
            info = dict()
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


class CVGenerator(object):
    def __init__(self, cv_info, *, lang='zh', private=True, education_misc=True):
        self.cv_info = deepcopy(cv_info)
        self.lang = lang
        self.private = private
        self.education_misc = education_misc
        if private:
            self._hide_sensitive()
        self.translation = {
            'zh': {
                'contact': '联系方式',
                'education': '教育经历',
                'education_table_header': ('时间', '学校', '学历', '专业', '其他'),
                'work': '工作经历',
                'internship': '实习经历',
                'campus_proj': '学校项目',
                'amateur': '业余项目',
                'misc': '自我评价'

            },
            'en': {
                'contact': 'Contact',
                'education': 'Education',
                'education_table_header': ('Time', 'University', 'Degree', 'Major', 'Misc'),
                'work': 'Working Experience',
                'internship': 'Internship',
                'campus_proj': 'Campus Projects',
                'amateur': 'Amateur Projects',
                'misc': 'Miscellaneous'
            },
        }[lang]

    @property
    def title(self):
        return [getattr(self, f'_{self.lang}_title'), '']

    @property
    def _zh_title(self):
        return f"# {self.cv_info['contact']['name']}"

    @property
    def _en_title(self):
        return f"# {self.cv_info['contact']['name_en']} {self._align_right(self.cv_info['contact']['name'])}"

    @property
    def contact(self):
        header = ['Email', 'TEL']
        info = ['[{email}](mailto:{email})'.format(email=self.cv_info['contact']['email']), self.cv_info['contact']['tel']]
        if self.cv_info['contact'].get('github_user', None):
            header.append('GitHub({github_followers,' + self.cv_info['contact']['github_user'] + '} followers)')
            info.append("[github.com/{github_user}](https://github.com/{github_user}/)".format(github_user=self.cv_info['contact']['github_user']))
        result = [f'## {self.translation["contact"]}', '', ]
        result.append(self._to_table_line(header))
        result.append(self._to_table_line(len(header)))
        result.append(self._to_table_line(info))
        result.extend(['', getattr(self, f"_{self.lang}_region"), '', ])
        return result

    @property
    def _zh_region(self):
        return self._align_right(self.cv_info['contact']['region'])

    @property
    def _en_region(self):
        return f"{self.cv_info['contact']['region_en']} {self._align_right(self.cv_info['contact']['region'])}"

    @property
    def education(self):
        if not self.cv_info['education']:
            return []
        table_header = self.translation['education_table_header']
        education_info = list()
        for education in self.cv_info['education']:
            education_info.append([education[key] for key in ['time', 'university', 'degree', 'major', 'edu_misc']])
        if not self.education_misc:
            table_header = table_header[:-1]
            education_info = [i[:-1] for i in education_info]
        result = [f'## {self.translation["education"]}', '', ]
        result.append(self._to_table_line(table_header))
        result.append(self._to_table_line(len(table_header)))
        for line in education_info:
            result.append(self._to_table_line(line))
        result.append('')
        return result

    @property
    def work(self):
        result = [f"## {self.translation['work']}", '']
        for work in self.cv_info['work']:
            result.extend((f"### {work['company']} {work['position']} {self._align_right(work['time'])}", ''))
            for proj in work['projects']:
                result.extend(self._project(proj, 4))
        return result

    @property
    def internship(self):
        return self._common_project_list('internship')

    @property
    def campus_proj(self):
        return self._common_project_list('campus_proj')

    @property
    def amateur(self):
        return self._common_project_list('amateur')

    @property
    def misc(self):
        result = ['## ' + self.translation['misc'], '']
        for item in self.cv_info['misc']:
            result.append('- ' + str(item))
        result.append('')
        return result

    def __str__(self):
        result = []
        for component in [
            'title',
            'contact',
            'education',
            'work',
            'internship',
            'campus_proj',
            'ameteur',
            'misc',
        ]:
            if hasattr(self, component):
                comp = getattr(self, component)
                if comp:
                    result.extend(comp)
        return '\n'.join(result)

    @staticmethod
    def _align_right(string):
        return f'<span style="float:right;">{string}</span>'

    @staticmethod
    def _to_table_line(items):
        if isinstance(items, int):
            items = ['----'] * items
        if isinstance(items, (list, tuple)):
            return '| ' + ' | '.join([str(i) for i in items]) + ' |'

    def _hide_sensitive(self):
        sensitive_keys = {
            'name', 'name_en', 'tel', 'region', 'region_en',
            'time', 'university', 'major', 'degree', 'edu_misc', 'company', 'position',
        }

        def traverse(info):
            if isinstance(info, dict):
                for k, v in info.items():
                    if k in sensitive_keys:
                        info[k] = k.upper()
                    else:
                        traverse(v)
            if isinstance(info, list):
                for v in info:
                    traverse(v)
        traverse(self.cv_info)

    def _project(self, info, level=4):
        result = list()
        title = f"{'#'*level} {info['proj_name']}"
        title_items = list()
        for key in ('company', 'time'):
            if info.get(key, None):
                title_items.append(str(info[key]))
        if title_items:
            title += self._align_right(' '.join(title_items))
        result.extend([title, ''])
        for key in ('situation', 'task', 'action', 'result'):
            if not info.get(key, None):
                continue
            result.append(f"- **{key[0].upper()}:** " + str(info[key]))
        for line in info.get('appendix', list()):
            result.append('- ' + line)
        result.append('')
        return result

    def _common_project_list(self, name, header_level=2, proj_level=4):
        if not self.cv_info.get(name, None):
            return []
        result = ['#' * header_level + ' ' + self.translation[name], '']
        for proj in self.cv_info[name]:
            result.extend(self._project(proj, proj_level))
        return result


cv_example = {
    'contact': {
        'name': '姓名',
        'name_en': 'Name',
        'email': 'Email@hide.tld',
        'tel': '+86 123456',
        'github_user': 'the0demiurge',
        'region': '太阳系 地球',
        'region_en': 'Solar System Earth',
    },
    'education': [
        {
            'time': '1984.1.1 - 1984.4.1',
            'university': '哈尔滨佛学院',
            'degree': '**本科**',
            'major': '佛学',
            'edu_misc': 'GPA: 3.6/Rank 5.6%',
        }
    ],
    'work': [
        {
            'company': '哈尔滨',
            'time': '1990.8.1 - 1990.8.2',
            'position': '佛学院主教',
            'projects': [
                {
                    'proj_name': '简历自动生成工具',
                    'situation': '找工作',
                    'task': '做个产品',
                    'action': '设计、编码、测试',
                    'result': '发布产品',
                    'appendix': ['github.com/the0demiurge'],
                }
            ]
        }
    ],
    'internship': [
        {
            'company': '哈尔滨佛寺',
            'time': '2019.6 - 2020.6',
            'proj_name': '佛学观察',
            'situation': '有花鸟观察需求',
            'task': '完成斑鸠的观察',
            'action': '捕获一只斑鸠',
            'result': '完成报告',
            'appendix': ['[报告链接](https://example.com)'],
        }
    ],
    'campus_proj': [
        {
            'time': '1234.6-1854.7',
            'proj_name': '访学',
            'situation': '求道',
            'task': None,
            'action': '研究',
            'result': '产出结果',
            'appendix': [],
        }
    ],
    'amateur': [
        {
            'time': '2020.1 - 2020.7',
            'proj_name': 'Shadow',
            'situation': '当时没有好用的ss订阅工具',
            'task': '做个自动订阅工具给自己用，也免费分享给大家',
            'action': '爬虫+网站',
            'result': 'github 项目获得 {github_star,the0demiurge,ShadowSocksShare} star',
            'appendix': ['[ss.pythonic.life](https://ss.pythonic.life)'],
        }
    ],
    'skills': [
        {
            'title': 'math',
            'items': [
                'dl',
                'rl',
                'or',
                'control',
            ]
        },
        {
            'title': 'engineering',
            'items': [
                'lang',
                'linux',
            ]
        }
    ],
    'misc': [
        '在线笔记: [notes.pythonic.life](https://notes.pythonic.life)'
    ]
}


def main(cv_info, *, lang='zh', private=True, education_misc=True):
    cv_generator = CVGenerator(cv_info, lang=lang, private=private, education_misc=education_misc)
    cv_filler = CVFiller()
    cv = str(cv_generator)
    return cv_filler.fill(cv)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cv-json', '-c', help='CV json path, use --example to get CV json example')
    parser.add_argument('--example', action='store_true')
    parser.add_argument('--lang', default='zh')
    parser.add_argument('--public', action='store_true', help='Show private information')
    parser.add_argument('--hide-education-misc', action='store_true', help='hide education misc information')
    return parser.parse_args()


if __name__ == '__main__':
    # convert to html:
    # pandoc cv.md -t html5 -o cv.html --self-contained --css=cv.css
    args = get_args()
    if args.example:
        print(json.dumps(cv_example, indent=4, ensure_ascii=False))
        exit()
    if not args.cv_json:
        print('use --help argument to show help messages')
        exit(1)
    cv_json = json.load(open(os.path.abspath(os.path.expanduser(args.cv_json))))
    print(main(cv_json, lang=args.lang, private=not args.public, education_misc=args.hide_education_misc))
