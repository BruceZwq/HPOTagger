# Part 1 (this part is consistent with PhenoTagger)

Preparation（git clone & pip install & setup.py）

# Part 2


## Instance-Enhancer


We use UMLS-MESH for all HPO data files for synonym augmentation in /your/path/PhenoTagger-enhancement/dict-Dsy/


## Semantic-Enhancer


We add model training parameters to the PhenoTagger_training.py file that can be used to represent our augmented models of pubmedberthposy_epoch_1/pubmedberthposy_epoch_10



# Part 3

# Integration Training

$ python PhenoTagger_training.py -t ... /data/distant_train_data/distant_train.conll -d ... /data/corpus/GSC/GSCplus_dev_gold.tsv -m pubmedberthposy_epoch_1 -o . /models/



