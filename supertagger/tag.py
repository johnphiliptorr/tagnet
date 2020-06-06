"""Code for testing a saved model"""

from lstm_model import LSTMTagger
from prepare_data import *
import argparse
import pdb
from file_handler import *
from utils import *
import copy

models_folder = 'models'


def main(data_path, dest_path, saved_model_path):
    EMBEDDING_DIM, CHAR_EMBEDDING_DIM, HIDDEN_DIM, CHAR_HIDDEN_DIM = load_hyper_params(saved_model_path)
    word_vocab, tag_vocab, char_to_ix = load_vocab_and_char_to_ix(saved_model_path)
    word_to_ix, ix_to_word, tag_to_ix, ix_to_tag = word_vocab.stoi, word_vocab.itos, tag_vocab.stoi, tag_vocab.itos
    sentences, sent_tensors = prepare_untagged_data(data_path, copy.deepcopy(word_to_ix))
    dest_file = open(dest_path, 'w')
    model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word_to_ix), len(tag_to_ix), CHAR_EMBEDDING_DIM, CHAR_HIDDEN_DIM,\
                       len(char_to_ix))
    load_model(model=model, saved_model_path=saved_model_path)
    #torch.autograd.set_detect_anomaly(True)
    print("\ntagging sentences using model: "+saved_model_path+'\n')
    model.eval()
    with torch.no_grad():
        sent_num = 0
        for sent_tensor in sent_tensors:
            sentence = sentences[sent_num]
            sent_num += 1
            word_batch_size = len(sentence)
            sent_batch_size = 1
            model.init_hidden(sent_batch_size)
            words_in = get_words_in(sent_tensor, char_to_ix, ix_to_word)
            tag_logits = model(sentences=sent_tensor,
                               words=words_in,
                               char_embedding_dim=CHAR_EMBEDDING_DIM,
                               char_hidden_dim=CHAR_HIDDEN_DIM,
                               sent_lengths=[len(sentence)],
                               word_batch_size=word_batch_size)
            pred = categoriesFromOutput(tag_logits, ix_to_tag)
            dest_file.write(" ".join(sentence)+'\t'+" ".join(pred)+'\n')
    dest_file.close()
    print("tagging complete")


if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser(description='command line arguments.')
    cmd_parser.add_argument('--data-path', dest='data_path', type=str, nargs=1, help='the path to the file containing the sentences to be tagged')
    cmd_parser.add_argument('--dest-path', dest='dest_path', type=str, nargs=1, help='the path to the file you want the tagged sentences to be saved in (file will be created/overwritten)')
    cmd_parser.add_argument('--model-path', dest='saved_model_path', type=str, nargs=1,
                            help='the relative path to the model you wish to resume training from')
    args = cmd_parser.parse_args()

    main(args.data_path[0], args.dest_path[0], args.saved_model_path[0])
