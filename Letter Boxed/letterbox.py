import sys
import string
import math
import numpy as np
from collections import deque

"""Simple solution to a generalized version of the word game "Letter Boxed" (as featured in the "Games" section of the New York Times Crossword page)"""

FACES = [list(set(face)) for face in sys.argv[1:-1]]

counter = 2
ENCODINGS = [] #to accommodate duplicate letters on different faces and facilitate indexing later on, each letter on the letterbox is assigned a unique prime number encoding.
CODES = []
for face in FACES:
	face_encodings = {}
	for letter in face:
		while(any(counter % i == 0 for i in range(2, int(counter**0.5) + 1))):
			counter += 1
		face_encodings[letter] = counter
		CODES.append(counter)
		counter += 1
	ENCODINGS.append(face_encodings)

TARGET = int(sys.argv[-1]) #Maximum solution length

def valid(word):
	"""Determine if a word can be formed with the specified letterbox."""

	for i in range(len(word)):
		if(i > 0):
			if(not any(word[i] in face and word[i - 1] in face_2 and face is not face_2 for face in FACES for face_2 in FACES)):
				return False
		if(i < len(word) - 1):
			if(not any(word[i] in face and word[i + 1] in face_2 and face is not face_2 for face in FACES for face_2 in FACES)):
				return False

	return True

def generate_key(word):
	"""Generates a numerical dictionary key unique to all anagrams of the supplied string 'word.'"""

	key = 1
	for i in range(len(word)):
		for face, encodings in zip(FACES, ENCODINGS):
			if(word[i] in face and (i == 0 or any(word[i - 1] in face_2 and face_2 is not face for face_2 in FACES)) 
			   and (i == len(word) - 1 or any(word[i + 1] in face_2 and face_2 is not face for face_2 in FACES))):
				key *= encodings[word[i]]

	return reduce_key(key)

def reduce_key(key):
	"""Helper function for generate_key(). Divides out redundant factors from the numerical key."""

	for code in CODES:
		while((key / code) % code == 0):
			key /= code

	return int(key)

def prod(iterable):
	"""Analogous to the built-in 'sum' function. Returns the product of integers from an iterator."""

	product = 1
	for item in iterable:
		product *= item

	return product

def bfs(words, traversal_order, faces, codes, target):
	"""Given a dictionary of valid letter:word list pairs, a list of letters determining the order in which said dictionary should be traversed, and the letterbox parameters, return all solutions to the problem."""

	solutions = []

	keys = {word:generate_key(word) for letter in words.keys() for word in words[letter]}

	path_log = {letter:{keys[word]:[word] for word in words[letter]} for face in faces for letter in face}

	fringe = deque(((key, word_list) for letter in traversal_order for key, word_list in path_log[letter].items()))

	goal = prod(codes)

	while(len(fringe) > 0):
		key, path = fringe.popleft()
		if(key == goal):
			yield path
			continue
		else:	
			required_letters = goal / key
			root = path[-1][-1]
			for prev_path in path_log[root].keys():
				if(prev_path % required_letters == 0 and len(path_log[root][prev_path]) + len(path) <= TARGET):
					yield path + path_log[root][prev_path]

			if(len(path) < math.ceil(target / 2)):
				path_log[path[0][0]][key] = path
		
			if(len(path) < target - 1):
				fringe.extend(((reduce_key(key * keys[word]), path + [word]) for word in words[root]))

		for word in words[path[-1][-1]]:
			new_path = path + [word]

#Construct a dictionary of word candidates.

with open('dict.txt', 'r') as f:
	words = {}
	for face in FACES:
		for letter in face:
			words.setdefault(letter, [])
	for word in f.readlines():
		word = word.strip('\n')
		if(len(word) >= 4 and all((any(letter in face for face in FACES) for letter in word)) and valid(word)):
			words[word[0]].append(word)

#Sort the words in decreasing order of cumulative letter 'scarcity.'

occurrences = np.zeros(26)

for first_letter in words.keys():
	for word in words[first_letter]:
		for letter in word:
			occurrences[ord(letter) - 97] += 1

for first_letter in words.keys():
	words[first_letter] = sorted(words[first_letter], key=lambda word: -1*sum((1 / occurrences[(ord(letter) - 97)] for letter in word)))

traversal_order = [chr(letter + 97) for letter in np.argsort(occurrences) if occurrences[letter] > 0]

#Return all solutions.

for solution in bfs(words, traversal_order, FACES, CODES, TARGET):
	print('—'.join(solution))




	