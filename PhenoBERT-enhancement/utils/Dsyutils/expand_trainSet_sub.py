def read_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            data.append((parts[0], parts[1]))
    return data

def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            file.write('\t'.join(item) + '\n')

def merge_files(file1, file2, file3):
    file1_data = read_file(file1)
    file2_data = read_file(file2)

    file1_ids = {item[1] for item in file1_data}

    new_items = []
    for id_ in file1_ids:
        if id_ == 'None':
            continue
        for item in file2_data:
            if item[1] == id_:
                new_items.append(item)

    merged_data = file1_data + new_items
    # 去重
    merged_data = list(dict.fromkeys(merged_data))

    write_file(file3, merged_data)

for i in range(23):
    print(i)
    merge_files('../../modelstrain_source\\train_' + str(i) + '.txt', 
    '../../models/Dsy_train.txt', 'new_train_source/train_'+str(i)+'.txt')
