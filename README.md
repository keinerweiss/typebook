# typebook

Inspired by ```typefortune``` which ships with [gtypist](https://www.gnu.org/savannah-checkouts/gnu/gtypist/gtypist.html), I wanted to create such typing lessons from my epub ebooks for gtypist.

Simply place typebook.py in your ~/bin/ folder and make it executable.

```
chmod u+x ~/bin/typebook.py
```

Requirements:
* gtypist
* ebook-convert from calibre
* python3

```
  sudo apt install calibre
  sudo apt install python3
  sudo apt install gtypist
```

Usage:
typebook.py <mode> <lessons> </path/to/ebook.epub>

Modes:
* line: get random sentences from the book
* word: get random word from the book; repeated 10x

Example:
```
typebook.py line 4 books/awesome-novel.epub
```
```
typebook.py word 6 books/awesome-novel.epub
```
Create gtypist lessons from ebooks
