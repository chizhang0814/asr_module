import os
import sys
words=sys.argv[1]
trans=sys.argv[2]
text=sys.argv[3]
output_file=sys.argv[4]

text_dict={}
all_text = open(text).readlines()
for line in all_text:
    wav_id = line.strip().split(' ')[0]
    gold = ' '.join(line.strip().split(' ')[1:])
    text_dict[wav_id]=gold
wd_dict={}
all_lines=open(words).readlines()

for ln in all_lines:
    wd_dict[ln.strip().split(' ')[1]]=ln.strip().split(' ')[0]

all_sent=open(trans).readlines()
fid = open(output_file,'w')
for sent in all_sent:
    
    tt = sent.strip().split(' ')
    sent_id = tt[0]
    ln = sent_id+' '
    for wd in tt[1:]:
        ln+=wd_dict[wd]+' '
    #ln = ln.strip()+','
    #gold=text_dict[sent_id]
    #ln+=gold+'\n'
    ln=ln.strip()+'\n'
    fid.write(ln)

    print(ln)
fid.close()

