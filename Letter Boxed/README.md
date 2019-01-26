#Letter Boxed

A simple solution to a generalized version of the word game "Letter Boxed" (as featured in the "Games" section of the New York Times Crossword page)

##Rules

The game is played on "letterboxes" of the following format:

```
 t — i — o
|	  |
y	  n
|	  |
l	  a	
|	  |
e	  x
 c — m — r
```

Given a target length N, the player is asked to form a list of at most N words that meets the following requirements:

- Every letter in the box appears at least once in the list.
- No two successive letters word are drawn from the same edge of the letterbox.
- Each successive word in the list begins with the final letter of the previous word.
- Each word contains at least 3 letters.

The sequence "exclaim"—"matrimony" solves the provided letterbox.

##Usage

```
python letterbox.py FACE_1 ... FACE_N TARGET
```

where the N face variables are strings of arbitrarily many lowercase letters corresponding to faces on an n-sided letterbox (e.g. 'abc') and TARGET is the maximum solution length.

##Example

```
python letterbox.py abcd ae trs bly por 3
```

##Acknowledgements

- dict.txt is derived from the 3of6game word list from [Alan Beale's 12dicts project] (http://wordlist.aspell.net/12dicts-readme/ "12dicts README").