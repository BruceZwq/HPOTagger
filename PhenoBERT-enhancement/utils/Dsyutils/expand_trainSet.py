import json


file_name = "Link_hpo_phenopro_umls_mesh_snomedct_synonyms_20221215_core_filter.json"
with open(file_name, 'r') as fin:
    with open("new_train.txt", "w") as fout:
        raw_data = json.load(fin)
        for hpoid in raw_data:
            textlist_set=set(raw_data[hpoid])
            for text in textlist_set:
                fout.write(text.strip()  + '\t' + hpoid.strip() + '\n')

with open('train-None.txt', 'r') as file1, open('new_train.txt', 'a') as file2:
    content = file1.read()
    file2.write(content)