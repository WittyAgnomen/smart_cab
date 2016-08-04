import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.A = ['forward', 'left', 'right',None] # all avaiable action
        self.trial = 0 # the number of trials
        self.Q = {} # Init Q table(light, next_waypoint)
	self.init_value=1.5 #the value to initilaize the q table with
        for i in ['green', 'red']:  # possible lights
            for j in ['forward', 'left', 'right']:  ## possible next_waypoints
                self.Q[(i,j)] = [self.init_value] * len(self.A)  ## linized Q table
	self.gamma = 0.3  # discount factor 
        self.alpha = 0.5  # learning rate
	self.epsilon = 0.1 # prob to act randomly, higher value means more exploration, more random action
	self.reward_holder='' #str to hold neg rewards and split term
	self.breaker=0 #value to calculate when new trial occurs
	

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'], self.next_waypoint)
        
        # TODO: Select action according to your policy
        #action = random.choice(self.env.valid_actions) # random action
        
	# Find the max Q value for the current state
        max_Q = self.Q[self.state].index(max(self.Q[self.state]))

        # assign action 
        p = random.random() #generate random value between 0 and 1
	#simulated annealing appraoch to avoid local opt, mainly to avoid staying in the same place      
	if p<=self.epsilon:
            action = random.choice(self.env.valid_actions)
        else:
            action = self.A[max_Q]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        '''
	#updating learning rate
        alpha_tune =500 # tunning parameter
        alpha = 1/(1.1+self.trial/alpha_tune) # decay learning rate
        self.trial = self.trial+1
	'''
        ## get the next state,action Q(s',a')
        next_inputs = self.env.sense(self)
        next_next_waypoint = self.planner.next_waypoint()
        next_state = (next_inputs['light'], next_next_waypoint)

        ## update Q table
        self.Q[self.state][self.A.index(action)] = \
            (1-self.alpha)*self.Q[self.state][self.A.index(action)] + \
	    (self.alpha * (reward + self.gamma * max(self.Q[next_state])))
       
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
	
	#to get an idea of penalties in later trials	
	if deadline>=self.breaker:
            self.reward_holder+='3 ' #will split string on 5 later and only be left with neg rewardfor a given trial
	self.breaker=deadline
	if reward<0:	
	    self.reward_holder+=str(reward)+' '

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    ## print Q table
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'final Q table'
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    for key in a.Q:
        print key,
        print ["%0.2f" % i for i in a.Q[key]]

    print '===================================================================='
    print 'An Array of Arrays where each subarray shows neg rewards for a trial'
    print '===================================================================='
    #print neg rewards and split term
    x=a.reward_holder.split('3')
    y=[i.split(' ') for i in x]
    print y #shows an array of arrays, could calculate total neg reward for each 
	    #trial, but no point; can easily see neg rewards even in later trials

if __name__ == '__main__':
    run()
