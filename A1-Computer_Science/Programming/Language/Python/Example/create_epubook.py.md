```python
from ebooklib import epub


def create_epubook(
    title,
    author,
    chapters: list,
    save_path,
    introduction=None,
    identifier=None,
    lang='zh',
):
    '''
    chapters = [
        (chapter, section, title, html_content),
    ]
    introduction = html_content
    '''
    book = epub.EpubBook()

    # add metadata
    if identifier is None:
        identifier = title
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(lang)

    book.add_author(author)

    spine = []
    intro_toc = []
    if introduction:
        filename = 'Introduction.xhtml'
        item = epub.EpubHtml(title='Introduction', file_name=filename, content=introduction)
        spine.append(item)
        book.add_item(item)
        intro_toc.append(epub.Link(filename, 'Introduction', 'intro'))
    sec_toc: list = [(epub.Section('placeholder'), list())]
    for i, (chapter, section, section_title, content) in enumerate(chapters):
        filename = f"{i}.xhtml"

        if chapter != sec_toc[-1][0].title:
            sec_toc.append((epub.Section(chapter, filename), list()))
        item = epub.EpubHtml(title=' '.join((section, section_title)), file_name=filename, content=content)

        sec_toc[-1][-1].append(item)

        spine.append(item)
        book.add_item(item)

    book.toc = intro_toc + sec_toc[1:]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = spine

    epub.write_epub(save_path, book, {})


if __name__ == '__main__':
    import tempfile
    _, path = tempfile.mkstemp(suffix='.epub')
    create_epubook(
        'title',
        'author',
        [
            ('c1', 's1', 'title for s1', 's1 content'),
            ('c1', 's2', 'title for s1', 's2 content'),
            ('c1', 's3', 'title for s1', 's3 content'),
            ('c2', 's1', 'title for s1', 's1 content'),
            ('c2', 's2', 'title for s1', 's2 content'),
            ('c2', 's3', 'title for s1', 's3 content'),
        ],
        path,
        introduction='introduction content'
    )
    print('saved at', path)

```
