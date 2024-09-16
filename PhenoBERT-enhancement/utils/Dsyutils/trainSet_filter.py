def filter_lines(input_file, output_file):
    data = {}
    
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            key = parts[0]
            value = parts[1]
            if key not in data:
                data[key] = value
            elif value.startswith('HP') and data[key] == 'None':
                data[key] = value

    with open(output_file, 'w') as output_f:
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) < 2:
                    continue
                key = parts[0]
                if parts[1] != 'None' or data[key] == 'None':
                    output_f.write(line)

# 调用函数并指定输入和输出文件
filter_lines('new_train.txt', '../../models/Dsy_train.txt')
