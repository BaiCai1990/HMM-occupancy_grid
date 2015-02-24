import numpy as np
import matplotlib.pyplot as plt

def forwardBackward(x,states,a_0,a,e,end_st):
	"""
	This is a forward-backward algorithm for inference in Hidden Markov Model.
	Assumption: The state transition probabilities, initial state probabilities and 
	observation probabilities are known. 
	Goal: Estimate the posterior probability of a state given observation and parameters.
	Computational Complexity is Big-Oh(number of observations * square of number of states)
	in case of finate states it is linear.
	"""
	L = len(x) #length of observation
	fwd = []
	f_prev = {}

	for i, x_i in enumerate(x):
		f_curr = {}
		for st in states: 
			if i == 0:
				prev_f_sum = a_0[st] # for the first term
			else:
				prev_f_sum = sum(f_prev[k]*a[k][st] for k in states) # update equation for forward algorithm 

			f_curr[st] = e[st][x_i]*prev_f_sum
		fwd.append(f_curr)
		f_prev = f_curr
	p_fwd = sum(f_curr[k]*a[k][end_st] for k in states)

	bkw = []
	b_prev ={}
	for i, x_i_plus in enumerate(reversed(x[1:]+(None,))):
		b_curr = {}
		for st in states :
			if i ==0:
				b_curr[st] = a[st][end_st] # last term update
			else:
				b_curr[st] = sum(a[st][l]*e[l][x_i_plus]*b_prev[l] for l in states) # update equation for backward algorithm

		bkw.insert(0,b_curr)
		b_prev = b_curr
	p_bkw = sum(a_0[l]*e[l][x[0]]*b_curr[l] for l in states)

	posterior =[]
	for i in xrange(L):
		posterior.append({st: fwd[i][st]*bkw[i][st]/p_fwd for st in states}) # calculating poseterior at each observation
	assert p_fwd == p_bkw
	return fwd,bkw,posterior

def forwards(x,states,a_0,a,e,end_state):
	"""
	This is a forwards algorithm for Hidden Markov Model. 
	Assumption: State transition probability(a), initial state probability(a_0) and observation probability(e) are known. 
	Goal: Comput the marginal posterior p(z_t | x_1:t)
	"""
	L = len(x) #length of observation
	fwd = []
	alpha_prev = {}
	for i, x_i in enumerate(x):
		alpha_curr = {}
		for st in states:
			if i == 0:
				prev_aplha_sum = a_0[st]
			else:
				prev_aplha_sum = sum(alpha_prev[k]*a[k][st] for k in states)
			alpha_curr[st]  = e[st][x_i]*prev_aplha_sum
		fwd.append(alpha_curr)
		alpha_prev = alpha_curr
	
	p_fwd = sum(alpha_curr[k]*a[k][end_state] for k in states)
	posterior = []
	for i in xrange(L):
		posterior.append({st: fwd[i][st]/p_fwd for st in states})
	print posterior

def viterbi(x,states,a_0,a,e):
	V= [{}]
	path = {}

	for y in states:
		V[0][y] = a_0[y]*e[y][x[0]]
		path[y] = [y]

	for t in xrange(1,len(x)):
		V.append({})
		newpath = {}

		for y in states:
			(prob,state) = max((V[t-1][y0]*a[y0][y]*e[y][x[t]],y0)for y0 in states )
			V[t]


if __name__ == '__main__':
	states = ('dynamic','static')
	end_state = 'static'
	observation = ('Occupied','Free','Unknown')
	start_probability = {'dynamic': 0.5,'static':0.5}  #with uniform initial probability
	transition_probability = {'dynamic':{'dynamic':0.5,'static':0.5},'static':{'dynamic':0.5,'static':0.5}}
	emission_probability = {'dynamic':{'Occupied':0.5,'Free':0.4,'Unknown':0.1},'static':{'Occupied':0.8,'Free':0.1,'Unknown':0.1}} # Heuristically determined 
	ex_observation = ('Free','Free','Free','Free','Free','Occupied','Occupied','Occupied','Occupied','Unknown','Occupied','Free','Occupied','Occupied','Occupied','Occupied')
	#fwd_pr,bkw_pr, posterior_pr = forwardBackward(ex_observation,states,start_probability,transition_probability,emission_probability,end_state)
	forwards(ex_observation,states,start_probability,transition_probability,emission_probability,states[0])