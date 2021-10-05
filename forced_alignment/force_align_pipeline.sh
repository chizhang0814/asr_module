#!/bin/bash



set -x
trn_dir=/opt/data/train_data/train_2020-12-05
ali_dir=${trn_dir}/exp/nnet2_online/nnet_ali_data_set_data_no1028_0912_1216_0108
mdl_dir=${trn_dir}/exp/nnet2_online/nnet_a/
ali_set=/opt/data/train_data/data_no1028_0912_1216_0108/data_set_data_no1028_0912_1216_0108


for i in ${ali_dir}/ali.*.gz; 
do 
  ali-to-phones --ctm-output ${mdl_dir}/final.mdl ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
done;

cat ${ali_dir}/*.ctm > ${ali_dir}/merged_alignment.txt
python3 id2phone_modify.py $trn_dir $ali_set $ali_dir
python3 split_alignment.py ${ali_dir}/final_ali.txt $ali_dir
python3 phon2pron.py  $ali_dir
