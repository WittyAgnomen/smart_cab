import random

class QL(object):
    def __init__(self, actions, q_0={}, alpha = 0.5, gamma = 0.5, default_q = 0.1):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.Q = q_0
        self.A = None
        self.newQ = -9999999999
        self.state0 = None
        self.action0 = None
        self.reward0 = None
        self.default_q = default_q    
    
    #function to get q value for particular state
    def getQ(self,state,action):
        if (state,action) not in self.Q:
            self.Q[(state,action)] = self.default_q
        return self.Q[(state,action)]
    
    def reset(self):
        (self.state0, self.action0, self.reward0) = (None, None, None)
    
    #get action
    def pickAction(self, state):
	self.newQ = -9999999999
        (x,y) = (0,0)
        self.A = None
	# if no difference in q for choice pick random
        while (y < len(self.actions)) & (x == 0):
            if self.getQ(state,self.actions[0]) == self.getQ(state,self.actions[y]):
                x = 1
            y += 1
        if x == 0:
            self.A = random.choice(self.actions)
	#else pick best action with hightest q
        else:
            for i in self.actions:
                if self.getQ(state,i) >= self.newQ:
                    self.newQ = self.getQ(state,i)
                    self.A = i
        return self.A
    
    #update state
    def updateState(self, state, reward, newAction = None):
        if newAction is not None:
            self.A = newAction
        if (self.state0, self.action0, self.reward0) != (None, None, None):
            oldQ = self.getQ(self.state0,self.action0)
            self.Q[(self.state0, self.action0)] = (1-self.alpha)*oldQ + self.alpha*(self.reward0 + self.gamma*self.newQ)
	(self.state0, self.action0, self.reward0) = (state, self.A, reward)


