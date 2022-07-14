```python
from typing import Tuple, Union

from ebooklib import epub


def create_epubook(
    title,
    author,
    chapters: list,
    save_path,
    *,
    cover_img: Tuple[str, Union[bytes, str]] = None,
    introduction: Tuple[str, str] = None,
    images: dict = None,
    identifier=None,
    lang='zh',
    css=None,
):
    '''
    chapters = [
        (chapter, section, html_content),
    ]
    cover_img = (filename, content)
    images = {filename: content}
    introduction = (title, html_content)
    '''
    book = epub.EpubBook()

    # add metadata
    if identifier is None:
        identifier = title
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(lang)

    book.add_author(author)

    if css is None:
        css = '''
body {
    text-align: justify;
}
img  {
    max-width: 100%;
    max-height: 100%;
    align: center;
}
'''
    style = epub.EpubItem(file_name='style/default.css', media_type='text/css', content=css)
    book.add_item(style)

    if cover_img is not None:
        book.set_cover(*cover_img, False)

    # images
    if images:
        for filename, img_content in images.items():
            item = epub.EpubImage(file_name=filename, content=img_content)
            book.add_item(item)

    spine = []

    # introduction
    intro_toc = []
    if introduction:
        if isinstance(introduction, str):
            introduction = ('Introduction', introduction)
        intro_title, intro_content = introduction
        filename = 'Introduction.xhtml'
        item = epub.EpubHtml(title=intro_title, file_name=filename, content=intro_content)
        spine.append(item)
        book.add_item(item)
        intro_toc.append(epub.Link(filename, intro_title, 'intro'))

    # sections
    sec_toc: list = [(epub.Section('placeholder'), list())]
    for i, (chapter, section, content) in enumerate(chapters):
        filename = f"chapter_{i}.xhtml"

        if chapter != sec_toc[-1][0].title:
            sec_toc.append((epub.Section(chapter, filename), list()))
        item = epub.EpubHtml(title=section, file_name=filename, content=content)

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

    img = b'<?xml version="1.0" encoding="utf-8" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <svg xmlns:xlink="http://www.w3.org/1999/xlink" width="460.8pt" height="345.6pt" viewBox="0 0 460.8 345.6" xmlns="http://www.w3.org/2000/svg" version="1.1"> <g> <path d="M 73.832727 295.488 L 398.487273 53.568 "  style="stroke: #ff7f0e; stroke-width: 1.5;"/> </g> </svg>'
    create_epubook(
        'title',
        'author',
        [
            ('c1', 'title for s1', '<p>s1 content</p><img src="1.svg"/>'),
            ('c1', 'title for s1', '<p>s2 content</p><img src="static/2.svg"/>'),
            ('c1', 'title for s1', '<p>s3 content</p>'),
            ('c2', 'title for s1', '<p>s1 content</p>'),
            ('c2', 'title for s1', '<p>s2 content</p>'),
            ('c2', 'title for s1', '<p>s3 content</p>'),
        ],
        path,
        introduction=('介绍', '<p>introduction content</p>'),
        cover_img=('cover.svg', img),
        images={
            '1.svg': img,
            'static/2.svg': img,
        }
    )
    print('saved at', path)

```
