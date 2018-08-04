import json
from gensim.models import FastText
from gensim.models import KeyedVectors
import torch
from torch.autograd import Variable
import numpy as np
import Encoder
import logging
import sys


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
model = torch.load('model/description_encoder')
# wv = KeyedVectors.load_word2vec_format('model/glove.6B.100d.txt.word2vec',
#                                        binary=False)
m = FastText.load('model/entity_fasttext_n100')
wv = m.wv
del m
punctuation = '!"#$%&\'()*+,.:;<=>?@[\\]^`{|}~'
table = str.maketrans('', '', punctuation)


def main(model, wv, abstracts_file, db_file):
    count = 0
    with open(abstracts_file, 'r') as input_file:
        with open(db_file, 'w+') as output_file:
            for line in input_file:
                print('INFO : {0}'.format(count), end='\r')
                # if count % 1000 == 0:
                #     logging.info(f'reading resource # {count}')
                db = {}
                json_line = json.loads(line)
                target = [_ for _ in json_line.keys()][0]
                # d = json_line[target]
                desc = json_line[target]['abstract']['value']
                desc = desc.translate(table).lower().split()
                if len(desc) > 10:
                    try:
                        r = np.array(list(map(lambda x: wv.get_vector(x),
                                              desc)),
                                     dtype=np.float32)
                    except KeyError:
                        continue
                    hidden = model.init_hidden()
                    for word in r:
                        try:
                            p, hidden = model(Variable(torch.tensor([[word]])),
                                              hidden)
                            p = p[0][0].detach().numpy()
                        except (TypeError, IndexError) as _:
                            continue
                    db[target] = p.tolist()
                    json.dump(db, output_file)
                    output_file.write('\n')
                    count += 1
                    # print('Entity : ' + target)
                    # print('Abstract : ' + d, end='')
                    # print('Predicted : ', end='')
                    # print(wv.similar_by_vector(p))
                    # output_file.write(target + '\n')
                    # output_file.write(d)
                    # output_file.write(str(p) + '\n')
                else:
                    continue


abstracts_file, db_file = sys.argv[1], sys.argv[2]
main(model, wv, abstracts_file, db_file)
