#!/bin/bash

show_usage() {
  echo "Usage: $0 <audio_folder>"
}

if [[ $# -lt 1 ]]; then
  show_usage
  exit 1
elif [[ ! -d "${1}" ]]; then
  echo "Error: \"${1}\" does not exist or it is not a folder!"
  show_usage
  exit 1
fi

. /opt/path.sh
. /opt/cmd.sh

#audio_batch_dir=/mnt/video/audio/2021-02-26/
audio_batch_dir="${1}"
wav_scp=$audio_batch_dir/wav.scp
model_dir=/opt/ASR_Models/
lmwt=10 #integeter
wip=0.0 #0.0|0.5|1.0
thread_num=`nproc --all`
if [ ! -f "$wav_scp" ]; then
  echo "$wav_scp is not existing"
  exit 0
fi

/opt/utils/fix_data_dir.sh $audio_batch_dir

## this version of the decoding treats each utterance separately
## without carrying forward speaker information.

decode_nj=`wc -l < "${audio_batch_dir}/utt2spk"`
if [ $decode_nj -gt $thread_num ]; then
  decode_nj=$thread_num
fi

/opt/scripts/asr_module/online_nnet3_decode.sh --online-config ${model_dir}/AM/conf/online.conf --acwt 1.0 --post-decode-acwt 10.0 --nj $decode_nj --cmd "$decode_cmd" --per-utt true ${model_dir}/graph $audio_batch_dir $audio_batch_dir/decode_tgsmall_chain_utt ${model_dir}/AM || exit 1


/opt/scripts/asr_module/print_hypo_text.sh  --cmd "$decode_cmd" --lmwt $lmwt --wip $wip $audio_batch_dir ${model_dir}/graph $audio_batch_dir/decode_tgsmall_chain_utt


/opt/steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" ${model_dir}/lang_tgsmall ${model_dir}/lang_vglarge $audio_batch_dir $audio_batch_dir/decode_tgsmall_chain_utt $audio_batch_dir/decode_vglarge_chain_utt


/opt/scripts/asr_module/print_hypo_text.sh  --cmd "$decode_cmd" --lmwt $lmwt --wip $wip $audio_batch_dir $model_dir/graph $audio_batch_dir/decode_vglarge_chain_utt

/opt/scripts/asr_module/generate_decode_word_segments.sh $audio_batch_dir decode_vglarge_chain_utt $model_dir $lmwt $wip  
