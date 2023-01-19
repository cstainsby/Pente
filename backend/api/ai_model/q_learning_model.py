
# --------------------------------------------------------------------------
# FILE: model.py
# NAME: Cole Stainsby
# DESC: Contains the implementation of the RL model which will be playing
#       the pente game. My work will be based off of the tensorflow 
#       documentation at:
#       https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial 
# --------------------------------------------------------------------------

import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common






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

    model = self.build_qnet_model()
    dqn = self.build_agent()
    

  def build_qnet_model(self, states, actions):

    # FROM tensorflow docs
    # QNetwork consists of a sequence of Dense layers followed by a dense layer
    # with `num_actions` units to generate one q_value per available action as
    # its output.

    model = tf.keras.Sequential()

    return model


  def build_agent(self, qnet_model, actions):
    # actions are which actions are availble to the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

    train_step_counter = tf.Variable(0)

    dqn = dqn_agent.DqnAgent(
      q_network=qnet_model,
      optimizer=optimizer,
      td_errors_loss_fn=common.element_wise_squared_loss,
      train_step_counter=train_step_counter
    )

    return dqn

  def dense_layer(num_units):
    return tf.keras.layers.Dense(
      num_units,
      activation=tf.keras.activations.relu,
      kernel_initializer=tf.keras.initializers.VarianceScaling(
          scale=2.0, mode='fan_in', distribution='truncated_normal')
    )

  def train(self):
    pass 

  def predict(self):
    pass 
  
  def save_model(self, dqn: dqn_agent.DqnAgent):
    dqn.save_weights()
