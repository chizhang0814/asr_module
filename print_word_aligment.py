import os,sys,glob

hypo_text = sys.argv[1]


pron_align_dir = sys.argv[2]
word_align_dir = sys.argv[3]

utt_id_text_dict = {}
all_lines = open(hypo_text).readlines()
for ln in all_lines:
    temp = ln.strip().split(' ')
    utt_id = temp[0]
    utt_id_text_dict[utt_id] = temp[1:] 

all_session_txt = glob.glob(pron_align_dir+'/*.txt')

for sess_align in all_session_txt:
    sess_id = sess_align.split('/')[-1].split('_speech.txt')[0]
    all_lines = open(sess_align).readlines()
    fid = open(word_align_dir+'/'+sess_id+'_word_align.txt','w')
    current_utt_id= ''
    for ln in all_lines:
        utt_id, wd, wd_st, wd_ed = ln.strip().split('\t')
        print('original: '+ln)
        if utt_id != current_utt_id:
            current_utt_id  = utt_id
            wd_count = 0
        if wd != 'SIL':
            new_ln = utt_id + '\t'+utt_id_text_dict[utt_id][wd_count]+'\t'+wd_st+'\t'+wd_ed+'\n'
            print('write: '+ new_ln)
            fid.write(new_ln)
            wd_count = wd_count+1
    fid.close()


  
   

    

