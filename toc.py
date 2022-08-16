#!/usr/bin/env python3
import os

basepath = os.path.abspath(os.path.expanduser(os.path.dirname(__file__)))
proj_name = 'CharlesNotes'


def format_line(name, link=None, level=0):
    if link:
        line = f"[{name}]({link})"
    else:
        line = name
    line = ' ' * 2 * level + '- ' + line
    return line


def traverse(path=basepath, level=-2):
    files = list()
    folders = list()
    readme = False
    for f in os.listdir(path):
        if f == 'README.md':
            readme = True
            continue
        if f.startswith('.') or f.startswith('_') or f in {'build', 'node_modules', 'SUMMARY.md'}:
            continue
        abspath = os.path.join(path, f)
        if os.path.isdir(abspath):
            folders.append(f)
        elif os.path.isfile(abspath) and f.lower().endswith('.md'):
            files.append(f)
    folders.sort()
    files.sort()
    root = path.replace(basepath, '', 1).lstrip(os.sep)
    if level >= 0:
        yield format_line(os.path.basename(root), os.path.join(root, 'README.md') if readme else None, level=level)
    for folder in folders:
        yield from traverse(os.path.join(path, folder), level=level + 2)
    if level >= 0:
        for file in files:
            yield format_line(os.path.splitext(file)[0], os.path.join(root, file), level=level + 1)


if __name__ == '__main__':
    with open('SUMMARY.md', 'w') as f:
        f.write('# ' + proj_name + '\n\n')
        for line in traverse():
            f.write(line + '\n')
