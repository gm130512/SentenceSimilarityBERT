date
#! /bin/bash
python3 my_run_classifier.py \
  --task_name=FAQ \
  --do_predict=true \
  --data_dir=$1 \
  --vocab_file=$2/vocab.txt \
  --bert_config_file=$2/bert_config.json \
  --init_checkpoint=$3 \
  --max_seq_length=128 \
  --output_dir=$4
  date
read -p "Press any key to continue." var
