#!/bin/bash
# Copyright 2012  Johns Hopkins University (Author: Daniel Povey)
#           2014  Guoguo Chen
#           2021  Chi Zhang@Appen
# Apache 2.0
# This script is heritaged from kaldi/egs/*/s5/local/score.sh

[ -f ./path.sh ] && . ./path.sh

# begin configuration section.
cmd=run.pl
stage=0
decode_mbr=true
wip=0.0
lmwt=7
iter=final
#end configuration section.

[ -f ./path.sh ] && . ./path.sh
. parse_options.sh || exit 1;

if [ $# -ne 3 ]; then
  echo "Usage: script/print_hypo_text.sh [--cmd (run.pl|queue.pl...)] <data-dir> <lang-dir|graph-dir> <decode-dir>"
  echo " Options:"
  echo "    --cmd (run.pl)                  # specify how to run the sub-processes."
  echo "    --decode_mbr (true/false)       # maximum bayes risk decoding (confusion network)."
  echo "    --lmwt <int>                    # LM-weight for lattice rescoring "
  echo "    --wip <0.0|0.5|1.0>             # word_ins_penalty for lattice rescoring "
  exit 1;
fi

data=$1
lang_or_graph=$2
dir=$3

symtab=$lang_or_graph/words.txt

for f in $symtab $dir/lat.1.gz; do
  [ ! -f $f ] && echo "print_tra.sh: no such file $f" && exit 1;
done

mkdir -p $dir/scoring/log

$cmd LMWT=$lmwt $dir/scoring/log/best_path.LMWT.$wip.log \
    lattice-scale --inv-acoustic-scale=LMWT "ark:gunzip -c $dir/lat.*.gz|" ark:- \| \
    lattice-add-penalty --word-ins-penalty=$wip ark:- ark:- \| \
    lattice-best-path --word-symbol-table=$symtab \
      ark:- ark,t:$dir/scoring/LMWT.$wip.tra || exit 1;

python3 /opt/scripts/asr_module/print_hypo_text_from_tra.py $symtab $dir/scoring/${lmwt}.${wip}.tra $dir/scoring/${lmwt}.${wip}.hypo.text

exit 0;
