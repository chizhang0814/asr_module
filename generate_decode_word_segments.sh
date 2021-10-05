. ./path.sh
. ./cmd.sh

if [ "$#" -ne 5 ]; then
    echo
    echo "  Usage: $0 batch_dir (eg. /mnt/video/audio/2021-03-30_my_postfix)"
    echo
    exit
fi

batch_dir=$1

decode_dir=${batch_dir}/$2 #${batch_dir}/decode_vglarge_chain_utt
model_dir=$3 #/opt/Models/
lmwt=$4 #10 #integeter
wip=$5 #0.0 #0.0|0.5|1.0
phones=${model_dir}/graph/phones.txt

rm ${decode_dir}/*.ali.gz
rm ${decode_dir}/*.ctm
rm -r ${decode_dir}/file_align
rm -r ${decode_dir}/pron_align
##lattice-best-path --acoustic-scale=0.1 ark:1.lats 'ark,t:|int2sym.pl -f 2- words.txt > text' ark:1.ali
for i in ${decode_dir}/lat.*.gz;
do
  echo $i
  echo ${model_dir}/graph/words.txt  
  lattice-best-path --acoustic-scale=1.0 --lm-scale=${lmwt} ark:"gunzip -c $i|" "ark,t:|int2sym.pl -f 2- ${model_dir}/graph/words.txt > text" ark:$i.ali
#  #lattice-best-path --acoustic-scale=10.0 --lm-scale=10 ark:'gunzip -c lat.1.gz|' 'ark,t:|int2sym.pl -f 2- /opt/Models/CHAIN_model/graph/words.txt > text' ark:1.ali
  gzip -f $i.ali
  ali-to-phones --frame-shift=0.03 --ctm-output ${model_dir}/AM/final.mdl ark:"gunzip -c $i.ali.gz|" -> ${i%.ali.gz}.ctm;
done;

cat ${decode_dir}/*.ctm > ${decode_dir}/merged_alignment.txt

python3 /opt/scripts/asr_module/forced_alignment/id2phone_modify.py $phones $batch_dir $decode_dir
python3 /opt/scripts/asr_module/forced_alignment/split_alignment.py ${decode_dir}/final_ali.txt $decode_dir
python3 /opt/scripts/asr_module/forced_alignment/phon2pron.py  $decode_dir
