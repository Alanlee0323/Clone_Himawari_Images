import struct

def read_data_range(file_path, start_row, end_row, start_column, end_column):
    with open(file_path, 'rb') as file:
        # 初始化存放數據的列表
        values = []

        # 迭代每一行
        for row in range(start_row, end_row):
            # 計算每一行的字節範圍
            row_start_byte = (row * 24000 + start_column) * 4
            row_end_byte = (row * 24000 + end_column) * 4
            
            # 定位到該行的開始位置
            file.seek(row_start_byte)

            # 讀取該行指定範圍的字節數據
            row_data = file.read(row_end_byte - row_start_byte)
            
            # 解析該行的浮點數值
            row_values = struct.unpack('f' * (end_column - start_column) , row_data)
            
            # 將該行的值添加到結果列表中
            values.extend(row_values)

        return values


def save_values_to_txt(values, file_path):
    with open(file_path, 'w') as file:
        for i in range(0, len(values), 200):
            line = ' '.join(str(value) for value in values[i:i+200])
            file.write(line + '\n')


# 調用函數讀取指定行和列範圍的數據
values = read_data_range(r'code\little-endian-201906040650.ext.01.fld.geossgrid05.dat', 
                         11800, 12000, 7800, 8000)

# 儲存values到txt檔
save_values_to_txt(values, r'code\5.txt')

def count_newlines(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        newline_count = content.count('\n')
        return newline_count

txt_file_path = r'code\5.txt'
newline_count = count_newlines(txt_file_path)
print(f"The number of newline characters in the txt file is: {newline_count}")


