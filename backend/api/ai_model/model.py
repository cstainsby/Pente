
# --------------------------------------------------------------------------
# FILE: model.py
# NAME: Cole Stainsby
# DESC: Contains the implementation of the RL model which will be playing
#       the pente game. My work will be based off of the tensorflow 
#       documentation at:
#       https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial 
# --------------------------------------------------------------------------

import tensorflow as tf


class PenteDeepQNetwork():

  def __init__(self) -> None:
    # define hyperparameters
    num_iterations = 20000 

    initial_collect_steps = 100
    collect_steps_per_iteration = 1
    replay_buffer_max_length = 100000

    batch_size = 64 
    learning_rate = 1e-3 
    log_interval = 200  

    num_eval_episodes = 10 
    eval_interval = 1000 


  def agent(self, policy):
    pass

  def train(self):
    pass 

  def predict(self):
    pass 
