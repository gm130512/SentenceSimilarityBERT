# SentenceSimilarityBERT
### 環境設定

```bash
# create the virtual envionment
$ python3 -m venv env

# activate the virtual environment
$ source env/bin/activate

# install dependencies
$ pip install -r requirements.txt
```
### SentenceSimilarityBERT 運行
```bash
# train
$ bash ./finetune_train.sh /<DATA_DIR_PATH>/ /<BERT_DIR_PATH>/ /<BERT_MODEL_PATH>/ /<OUTPUT_PATH>/

# test
$ bash ./finetune_test.sh /<DATA_DIR_PATH>/ /<BERT_DIR_PATH>/ /<TRAINED_BERT_MODEL>/ /<OUTPUT_PATH>/
```