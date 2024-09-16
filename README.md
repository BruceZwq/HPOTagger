# HPOTagger
<<<<<<< HEAD

Investigation of Synonym Expansion and Self-Alignment Pretraining for Enhancing Human Phenotype Ontology Concept Recognition


# Instance enhancement

Go to the official websites of UMLS and MESH to download the synonym expansion files:

UMLS: https://www.nlm.nih.gov/research/umls/licensedcontent/umlsarchives04.html

MESH: https://www.nlm.nih.gov/databases/download/mesh.html

# Semantic enhancement

Refer to SapBERT model training process:

1. Replace the UMLS synonym file in SapBERT with the HPO synonym expansion file in the first step.

2. Use the SapBERT training script to train 1(10) rounds, and output the model file as the subsequent semantic enhancement model.

# Model Training and Tagging

Go to read the readmes at /your/path/PhenoTagger-enhancement/ and /your/path/PhenoBERT-enhancement/ for the corresponding Training and Tagging.
=======
Investigation of Synonym Expansion and Self-Alignment Pretraining for Enhancing Human Phenotype Ontology Concept Recognition
>>>>>>> 1d9441ad44091045931041bdfa44f87fc2987b38
