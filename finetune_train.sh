date

python3 my_run_classifier.py \
  --task_name=FAQ \
  --do_train=true \
  --do_eval=true \
  --data_dir=$1 \
  --vocab_file=$2/vocab.txt \
  --bert_config_file=$2/bert_config.json \
  --init_checkpoint=$3 \
  --max_seq_length=128 \
  --train_batch_size=8 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$4

date

read -p "Press any key to continue." var
