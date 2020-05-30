"""The neural network model.  Contains LSTMs for both words and characters"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import pdb

class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size, char_embedding_dim, char_hidden_dim,
                 char_vocab_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.char_hidden_dim = char_hidden_dim

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.char_embeddings = nn.Embedding(char_vocab_size, char_embedding_dim)
        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(embedding_dim + char_hidden_dim, hidden_dim)
        self.char_lstm = nn.LSTM(char_embedding_dim, char_hidden_dim)
        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def init_hidden(self, sent_batch_size):
        # Before we've done anything, we dont have any hidden state.
        # Refer to the Pytorch documentation to see exactly
        # why they have this dimensionality.
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        return (torch.zeros(1, sent_batch_size, self.hidden_dim),
                torch.zeros(1, sent_batch_size, self.hidden_dim))

    def init_char_hidden(self, word_batch_size):
        # Before we've done anything, we dont have any hidden state.
        # Refer to the Pytorch documentation to see exactly
        # why they have this dimensionality.
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        return (torch.zeros(1, word_batch_size, self.char_hidden_dim),
                torch.zeros(1, word_batch_size, self.char_hidden_dim))

    def forward(self, sentences, words, char_embedding_dim, char_hidden_dim):
        sent_len = sentences.shape[0]
        sent_batch_size = sentences.shape[1]
        embeds = self.word_embeddings(sentences)
        char_final_hiddens = torch.zeros(sent_len, sent_batch_size, char_hidden_dim, requires_grad=False)
        for sent in range(sent_batch_size):
            word_len = words[sent].shape[0]
            char_embeds = self.char_embeddings(words[sent])
            # we treat each sentence as a batch of words for the char LSTM, hence batch size = sent_len
            _, self.char_hidden = self.char_lstm(char_embeds.view(word_len, sent_len, -1), self.char_hidden)
            char_final_hiddens[:,sent,:] = self.char_hidden[0]
        embeds = torch.cat((embeds, char_final_hiddens), dim=2)
        pdb.set_trace()
        lstm_out, self.hidden = self.lstm(
            embeds.view(len(sentence), 1, -1), self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores