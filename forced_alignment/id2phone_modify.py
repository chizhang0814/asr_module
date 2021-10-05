import os
import sys

phones_f=sys.argv[1]
ali_set=sys.argv[2]
ali_dir=sys.argv[3]

phones=open(phones_f).readlines()
print("Read phones Done")

ph_dict = {}

for ln in phones:
    ph, ph_id = ln.strip().split(' ')
    ph_dict[ph_id]=ph 




print("Read segments")
segments=open(ali_set+"/segments").readlines()
seg_dict = {}
for ln in segments:
    utt_id, wav_id, seg_st, seg_ed = ln.strip().split(' ')
    seg_dict[utt_id] = [wav_id, seg_st, seg_ed]

print("Read segments Done")

ctm=open(ali_dir+"/merged_alignment.txt").readlines()
print("Read merged_alignment")
fid = open(ali_dir+"/final_ali.txt",'w')
fid.write("file_utt\tfile\tid\tutt\tstart\tdur\tphone\tstart_utt\tend_utt\tstart_real\tend_real\n")
for ln in ctm:
    utt_id, utt, st, dur, ph_id = ln.strip().split(' ')
    wav_id, seg_st, seg_ed = seg_dict[utt_id]
	
    fid.write('\t'.join([utt_id, wav_id, ph_id, utt, st, dur, ph_dict[ph_id], seg_st, seg_ed, str(round(float(seg_st)+float(st),3)),str(round(float(seg_st)+float(st)+float(dur),3))])+'\n')    


fid.close()


