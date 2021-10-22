# CS421: Natural Language Processing
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




# Class definition for Hidden Markov Model (HMM)
# Do not make any changes to this class
# You are not required to understand the inner workings of this class
class HMM:
	"""
		Arguments:

		states: Sequence of strings representing all states
		vocab: Sequence of strings representing all unique observations
		trans_prob: Transition probability matrix. Each cell (i, j) contains P(states[j] | states[i])
		obs_likelihood: Observation likeliood matrix. Each cell (i, j) contains P(vocab[j] | states[i])
		initial_probs: Vector representing initial probability distribution. Each cell i contains P(states[i] | START)
	"""
	def __init__(self, states, vocab, trans_prob, obs_likelihood, initial_probs):
		self.states = states
		self.vocab = vocab
		self.trans_prob = trans_prob
		self.obs_likelihood = obs_likelihood
		self.initial_probs = initial_probs

    # Function to return transition probabilities P(q1|q2)
	def tprob(self, q1, q2):
		if not (q1 in self.states and q2 in ['START'] + self.states):
			raise ValueError("invalid input state(s)")
		q1_idx = self.states.index(q1)
		if q2 == 'START':
			return self.initial_probs[q1_idx]
		q2_idx = self.states.index(q2)
		return self.trans_prob[q2_idx][q1_idx]
    
    # Function to return observation likelihood P(o|q)
	def oprob(self, o, q):
		if not o in self.vocab:
			raise ValueError('invalid observation')
		if not (q in self.states and q != 'START'):
			raise ValueError('invalid state')
		obs_idx = self.vocab.index(o)
		state_idx = self.states.index(q)
		return self.obs_likelihood[obs_idx][state_idx]
	
	# Function to retrieve all states
	def get_states(self):
		return self.states.copy()


# Function to initialize an HMM using the weather-icecream example in Figure 6.3 (Jurafsky & Martin v2)
# Do not make any changes to this function
# You are not required to understand the inner workings of this function
def initialize_icecream_hmm():
	states = ['HOT', 'COLD']
	vocab = ['1', '2', '3']
	tprob_mat = [[0.7, 0.3], [0.4, 0.6]]
	obs_likelihood = [[0.2, 0.5], [0.4, 0.4], [0.4, 0.1]]
	initial_prob = [0.8, 0.2]
	hmm = HMM(states, vocab, tprob_mat, obs_likelihood, initial_prob)
	return hmm


# Function to implement viterbi algorithm
# Arguments:
# hmm: An instance of HMM class as defined in this file
# obs: A string of observations, e.g. ("132311")
# Returns: seq, prob
# Where, seq (list) is a list of states showing the most likely path and prob (float) is the probability of that path
# Note that seq sould not contain 'START' or 'END' and In case of a conflict, you should pick the state at lowest index
def viterbi(hmm, obs):
	# [YOUR CODE HERE]
	states = hmm.get_states()
	states_len = len(states)
	viterbi_values = [[0 for j in range(states_len)] for i in range(len(obs))]
	backtracking_matrix = [[0 for j in range(states_len)] for i in range(len(obs))]
	for j in range(states_len):
		viterbi_values[0][j] = hmm.tprob(states[j], 'START') *hmm.oprob(obs[0], states[j])
		backtracking_matrix[0][j] = -1
	for i in range(1, len(obs)):
		for j in range(states_len):
			index, viterbi_values[i][j] = v_max(viterbi_values[i-1], obs[i], j, states, hmm)
			backtracking_matrix[i][j] = index
	hidden_state_sequence, prob = backtrack(viterbi_values, backtracking_matrix, states)
	return reversed(hidden_state_sequence), prob

def backtrack(viterbi_values, backtracking_matrix, states):
	obs = len(viterbi_values)
	hidden_state_sequence = []
	prob = max(viterbi_values[obs-1])
	last_state = viterbi_values[obs-1].index(prob)
	hidden_state_sequence.append(states[last_state])
	for i in reversed(range(1, obs)):
		last_state = backtracking_matrix[i][last_state]
		hidden_state_sequence.append(states[last_state])
	return hidden_state_sequence, prob
	

def v_max(viterbi_value_1, observation, state_index, states, hmm):
	states_len = len(states)
	new_viterbi_value = []
	for j in range(states_len):
		new_viterbi_value.append(viterbi_value_1[j] * hmm.tprob(states[state_index], states[j]) * hmm.oprob(observation, states[state_index]))
	prob = max(new_viterbi_value)
	new_state_index = new_viterbi_value.index(prob)
	return new_state_index, prob


# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 q3.py
# It should produce the following output:
# 		  $python3 q3.py
#         P(HOT|COLD) = 0.4
#         P(COLD|START) = 0.2
#         P(1|COLD) = 0.5
#         P(2|HOT) = 0.4
#         Path: ['HOT', 'COLD']
#         Probability: 0.2

def main():
	# We can initialize our HMM using initialize_icecream_hmm function
	hmm = initialize_icecream_hmm()

	# We can retrieve all states as
	print("States: {0}".format(hmm.get_states()))

	# We can get transition probability P(HOT|COLD) as
	prob = hmm.tprob('HOT', 'COLD')
	print("P(HOT|COLD) = {0}".format(prob))

	# We can get transition probability P(COLD|START) as
	prob = hmm.tprob('COLD', 'START')
	print("P(COLD|START) = {0}".format(prob))

	# We can get observation likelihood P(1|COLD) as
	prob = hmm.oprob('1', 'COLD')
	print("P(1|COLD) = {0}".format(prob))

	# We can get observation likelihood P(2|HOT) as
	prob = hmm.oprob('2', 'HOT')
	print("P(2|HOT) = {0}".format(prob))

	# You should call the viterbi algorithm as
	path, prob = viterbi(hmm, "13213")
	print("Path: {0}".format(path))
	print("Probability: {0}".format(prob))


################ Do not make any changes below this line ################
if __name__ == '__main__':
    exit(main())