# Part 1 (this part is consistent with PhenoBERT)

Preparation（git clone & pip install & setup.py）

Download files in embeddings directory (biobert_v1.1_pubmed & pubmedberthposy_epoch_10_filter & fasttext_pubmed.bin)

# Part 2

## Semantic-Enhancer

```
# Replace 'biobert_v1.1_pubmed' in the path with 'pubmedberthposy_epoch_10_filter'.
```

## Instance-Enhancer

```
# Generate the original training dataset.
cd /your/path/PhenoBERT-enhancement/utils
python produce_trainSet.py
python produce_trainSet_sub.py

# Expand CNN layer1 training dataset.
cd /your/path/PhenoBERT-enhancement/utils/Dsyutils
python extractNone.py
python expand_trainSet.py
python trainSet_filter.py

# Expand CNN layer2 training dataset.
cd /your/path/PhenoBERT-enhancement/utils/Dsyutils
python expand_trainSet_sub.py
python trainSet_sub_filter.py

# After these steps, the Dsy_train.txt file and Dsy_train_source folder will be in /your/path/PhenoBERT-enhancement/models/.
```

