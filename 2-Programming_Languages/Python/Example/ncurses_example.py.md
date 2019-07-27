```python
import curses
import locale
from curses import textpad
from math import ceil

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

msgs = list()
stdscr = curses.initscr()
# curses.noecho()
curses.cbreak()

len_contact = 20
contacts = curses.newwin(curses.LINES, len_contact, 0, 0)
messages = curses.newwin(curses.LINES, curses.COLS - len_contact, 0, len_contact)


attrs = {'curses.A_BLINK': curses.A_BLINK,
         'curses.A_BOLD': curses.A_BOLD,
         'curses.A_DIM': curses.A_DIM,
         'curses.A_REVERSE': curses.A_REVERSE,
         'curses.A_STANDOUT': curses.A_STANDOUT,
         'curses.A_UNDERLINE': curses.A_UNDERLINE, }
for i, attr in enumerate(attrs):
    contacts.addstr(i+2, 1, attr, attrs[attr])
contacts.addstr(1, 1, '测试')
contacts.border()
messages.border()
textpad.rectangle(messages, curses.LINES-4, 1, curses.LINES-2, curses.COLS-len_contact-2)
stdscr.refresh()
contacts.refresh()
messages.refresh()
try:
    for index in range(100):
        msglen = curses.COLS-len_contact-4
        msgheight = curses.LINES - 5
        data = messages.getstr(curses.LINES - 3, 2, msglen).decode('utf-8')
        data = [['> ', '  '][i != 0] + data[msglen * i:msglen*(i+1)] for i in range(ceil(len(data)/msglen))]
        msgs.extend(data)

        for j, info in zip(range(msgheight), msgs[-(msgheight):]):
            messages.addstr(j+1, 1, ' ' * (curses.COLS - len_contact - 2))
            messages.addstr(j+1, 1, info)

        messages.addstr(curses.LINES-3, 2, ' ' * msglen)
        messages.border()
        contacts.border()
        textpad.rectangle(messages, curses.LINES-4, 1, curses.LINES-2, curses.COLS-len_contact-2)
        messages.refresh()
        contacts.refresh()
        messages.getch()
        curses.getmouse()
except KeyboardInterrupt:
    curses.endwin()
```