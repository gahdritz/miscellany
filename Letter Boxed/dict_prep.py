import numpy as np
import string

"""Transforms 3of6dict.txt into a dictionary for use by letterbox.py"""

trans_table = str.maketrans("", "", string.punctuation)
with open('3of6game.txt', 'r') as f:
	words = []
	for word in f.readlines():
		word = word.translate(trans_table)
		if(len(word) - 1 >= 3):
			words.append(word)

with open('dict.txt', 'w') as f:
	for word in words:
		f.write(word)