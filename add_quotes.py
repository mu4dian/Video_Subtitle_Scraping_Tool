def add_quotes_to_each_line(input_file, output_file):
    """
    读取输入文件的每一行，在行首和行尾添加双引号，
    并将结果写入到输出文件中。

    参数：
        input_file: 输入文件路径（包含原始文本）
        output_file: 输出文件路径（保存处理后的文本）
    """
    # 读取所有行
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    # 处理每一行并写入新文件
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in lines:
            # 去除行尾的换行符
            line = line.rstrip('\n')
            # 给每一行两端添加双引号
            quoted_line = f'"{line}"'
            # 写入并换行
            f_out.write(quoted_line + "\n")


if __name__ == '__main__':
    # 输入文件路径，例如 'input.txt'
    input_file = 'input.txt'
    # 输出文件路径，例如 'output.txt'
    output_file = 'add_quotes.txt'
    add_quotes_to_each_line(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")
