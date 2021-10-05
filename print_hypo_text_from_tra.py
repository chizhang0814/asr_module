import os
import sys

# This script is to print the ASR decoded result in text
# *.tra is the ASR decoded result in integer, each integer is mapping to a word in graphdir/words.txt

words=sys.argv[1]
trans=sys.argv[2]
hypo_text=sys.argv[3]

wd_dict={}
#all_lines=open(words).readlines()
all_lines=open(words, 'r', encoding='utf-8').readlines()
for ln in all_lines:
    wd_dict[ln.strip().split(' ')[1]]=ln.strip().split(' ')[0]

all_sent=open(trans).readlines()
#fid = open('result_comparison.csv','w'
fid = open(hypo_text,'w', encoding='utf-8')
for sent in all_sent:
    tt = sent.strip().split(' ')
    sent_id = tt[0]
    ln = sent_id+' '
    for wd in tt[1:]:
        '''
        try:
            ln+=wd_dict[wd]+' '
        except:
            ln+=wd+' '
        '''
        ln+=wd_dict[wd]+' '
    ln = ln.strip()+'\n'
    fid.write(ln)
fid.close()

