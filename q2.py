# CS 421: Natural Language Processing
# University of Illinois at Chicago
# Fall 2021
# Assignment 3
#
# Do not rename/delete any functions or global variables provided in this template and write your solution
# in the specified sections. Use the main function to test your code when running it from a terminal.
# Avoid writing that code in the global scope; however, you should write additional functions/classes
# as needed in the global scope. These templates may also contain important information and/or examples
# in comments so please read them carefully. If you want to use external packages (not specified in
# the assignment) then you need prior approval from course staff.
# This part of the assignment will be graded automatically using Gradescope.
# =========================================================================================================

import numpy as np
from utils import *


# Function to get word2vec representations
# Arguments:
# docs: A list of strings, each string represents a document
# Returns: mat (numpy.ndarray) of size (len(docs), dim)
# mat is a two-dimensional numpy array containing vector representation for ith document (in input list docs) in ith row
# dim represents the dimensions of word vectors, here dim = 300 for Google News pre-trained vectors
def word2vec_rep(docs):
	# [Your code here]
	# Dummy matrix
	dim = 300
	mat = np.zeros((len(docs), dim))
	new_docs = []
	for document in docs:
		new_docs.append(preprocessing(document))
	w2v = load_w2v()
	for i, doc in enumerate(new_docs):
		mat[i] = string2vec(w2v, doc)
	return mat

def w2v(word2vec, token):
    word_vector = np.zeros(300,)
    if token in word2vec.keys():
        return word2vec[token]
    return word_vector


def string2vec(word2vec, user_input):
    embedding = np.zeros(300,)
    preprocessed_input = preprocessing(user_input)
    tokens = get_tokens(preprocessed_input)
    for token in tokens:
        embedding+=w2v(word2vec, token)
    embedding = embedding/len(tokens)
    return embedding

# Use the main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 q2.py
# It should produce the following output:
#
# $ python3 q2.py
# Tokens for first document: ['Many', 'buildings', 'at', 'UIC', 'are', 'designed', 'in', 'the', 'brutalist', 'style']
# Is 'he' a stopword? True
# Is 'hello' a stopword? False
# Is 'she' a stopword? True
# Is 'uic' a stopword? False

def preprocessing(user_input):
    # Initialize modified_input to be the same as the original user input
    modified_input = user_input

    # Write your code here:
    tokens = get_tokens(user_input)
    no_stop = []
    for t in tokens:
        if t not in get_stopwords():
            no_stop.append(t.lower())
    modified_input = ' '.join(no_stop)
    return modified_input

def main():
	# Initialize the corpus
	sample_corpus = ['Many buildings at UIC are designed in the brutalist style.',
					'Brutalist buildings are generally characterized by stark geometric lines and exposed concrete.',
					'One famous proponent of brutalism was a Chicago architect named Walter Netsch.',
					'Walter Netsch designed the entire UIC campus in the early 1960s.',
					'When strolling the campus and admiring the brutalism, remember to think of Walter Netsch!']
	
	# We can tokenize the first document as
	tokens = get_tokens(sample_corpus[0])
	print("Tokens for first document: {0}".format(tokens))

	documents = [preprocessing(document) for document in sample_corpus]

	# We can fetch stopwords and check if a word is a stopword
	stopwords = get_stopwords()
	for word in ['he', 'hello', 'she', 'uic']:
		answer = word in stopwords
		print("Is '{0}' a stopword? {1}".format(word, answer))
	
	# We can load numpy word vectors using load_w2v as
	# w2v = load_w2v()
	# And access these vectors using the dictionary
	# print(w2v['chicago'])
	mat = word2vec_rep(sample_corpus)
	print(mat)
	
	

################ Do not make any changes below this line ################
if __name__ == '__main__':
	main()
