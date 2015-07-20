#!/usr/bin/python

import os
import sys
import h5py
import pdb
import re


SENTENCE_SPLIT_REGEX = re.compile(r'(\W+)')
def split_sentence(sentence):
    # break sentence into a list of words and punctuation
    sentence = [ s.lower().strip() for s in SENTENCE_SPLIT_REGEX.split(sentence.strip()) if len(s.strip()) > 0]
    # remove the '.' from the end of the sentence
    if sentence[-1] != '.':
        # print "Warning: sentence doesn't end with '.'; ends with: %s" % sentence[-1]
        return sentence
    return sentence[:-1]

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Usage: {0} <SBU_caption> <SBU_url> <fea_dir_train_dist_mapping_fns.txt> <stop_words> [top = 10]'.format(sys.argv[0])
        sys.exit()

    sbu_cap = sys.argv[1]
    sbu_url = sys.argv[2]
    dist_mapping_fns = sys.argv[3]
    stop_words = sys.argv[4]
    dict_stop_words = {}
    top = 10
    if len(sys.argv) >= 6:
        top = int(sys.argv[5])

    with open(stop_words, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            dict_stop_words[aline] = 1

    sbu_img2dict = {}
    with open(sbu_url,'r') as fid_url:
        with open(sbu_cap,'r') as fid_cap:
            for url,cap in zip(fid_url, fid_cap):
                url = url.strip()
                cap = cap.strip()
                sbu_img2dict[os.path.basename(url)] = cap
    
    save_fn = os.path.splitext(os.path.basename(dist_mapping_fns))[0]
    save_fn = 'key_words_' + save_fn + '.txt'
    fidw = open(save_fn, 'w')
    with open(dist_mapping_fns, 'r') as fid:
        for aline in fid:
            parts = aline.strip().split()
            words = {}
            for ref in parts[1:]:
                key = os.path.basename(ref)
                cap = sbu_img2dict[key]
                cap_words = split_sentence(cap)
                for word in cap_words:
                    if word not in dict_stop_words:
                        if word not in words:
                            words[word] = 0
                        words[word]  += 1
            word_list = sorted(words.items(), key = lambda x: x[1] , reverse = True)
            print >>fidw, parts[0], [ word[0] for word in word_list[0:top] ]

    fidw.close()
    print 'done with', save_fn



