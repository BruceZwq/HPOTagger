def filter_lines(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    filtered_lines = [line for line in lines if line.strip().split('\t')[1] == 'None']

    with open(output_file, 'w') as f:
        f.writelines(filtered_lines)

# 调用函数并指定输入和输出文件
filter_lines('../../models/train.txt', 'train-None.txt')
