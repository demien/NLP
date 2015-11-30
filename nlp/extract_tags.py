# encoding=utf-8
import sys
sys.path.append('../')

import jieba
import jieba.analyse
import jieba.posseg as pseg
from optparse import OptionParser

USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

content = open(file_name, 'rb').read()


def extract_tags(content, topK=topK):
    # tags = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)
    tags = jieba.analyse.extract_tags(content, topK=topK)
    print(",".join(tags))


def cut(content):
    seg_list = pseg.cut(content)
    for word, flag in seg_list:
        if flag in ['n', 'nr', 'ns', 'nz', 'nl', 'ng', 's', 'v']:
            print('%s %s' % (word, flag))


# extract_tags(content, topK)
cut(content)
