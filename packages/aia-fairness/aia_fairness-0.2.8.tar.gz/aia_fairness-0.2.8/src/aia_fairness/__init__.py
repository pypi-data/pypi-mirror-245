import numpy as np
import torch
import silence_tensorflow.auto
import tensorflow as tf

from .config import random_state
np.random.seed(random_state)
torch.manual_seed(random_state)
tf.random.set_seed(random_state)
tf.keras.utils.set_random_seed(random_state)
