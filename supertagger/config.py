"""Configuration of hyperparameters for the supertagger"""

#Parameters which are saved and loaded with the model (these are only laoded from this file if training a model from scratch):

embedding_dim = 128
char_embedding_dim = 32
hidden_dim = 128
char_hidden_dim = 56
use_bert_cased = False
use_bert_uncased = True
use_bert_large =  False

#Parameters which are not saved (these will always be loaded from this file even when a saved model is loaded)

num_epochs = 100
batch_size = 4
learning_rate = 0.001
weight_decay = 0
use_cuda_if_available = True
data_parallel = False