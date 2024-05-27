import struct
import os

def read_data_range(file_path, start_row, end_row, start_column, end_column):
    # 開啟指定的二進位文件
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
            
            # 檢查讀取的數據長度是否正確
            expected_length = (end_column - start_column) * 4
            if len(row_data) != expected_length:
                raise ValueError(f"預期 {expected_length} 字節，但獲得 {len(row_data)} 字節")

            # 將字節數據解析為浮點數
            row_values = struct.unpack('f' * (end_column - start_column), row_data)
            values.extend(row_values)

        return values


def save_values_to_txt(values, file_path, end_column, start_column):
    # 開啟指定的文本文件以寫入數據
    with open(file_path, 'w') as file:
        # 每200個數據一行寫入
        for i in range(0, len(values), (end_column - start_column)):
            line = ' '.join(str(value) for value in values[i:i+(end_column - start_column)])
            file.write(line + '\n')


def count_newlines(file_path):
    # 開啟文本文件並讀取內容
    with open(file_path, 'r') as file:
        content = file.read()
        # 計算文件中的換行符數量
        newline_count = content.count('\n')
        return newline_count


def get_user_input():
    # 循環直到獲得有效的用戶輸入
    while True:
        try:
            # 獲取文件夾路徑
            folder_path = input("輸入包含文件的文件夾路徑: ").strip()
            if not os.path.isdir(folder_path):
                raise ValueError("提供的文件夾路徑不存在。")
            
            # 獲取行和列範圍
            start_row = int(input("Enter start_row: ").strip())
            end_row = int(input("Enter End_row: ").strip())
            start_column = int(input("Enter start_column: ").strip())
            end_column = int(input("Enter end_column: ").strip())

            # 檢查行和列範圍的有效性
            if start_row < 0 or end_row <= start_row:
                raise ValueError("結束行必須大於起始行，且兩者必須是非負數。")
            if start_column < 0 or end_column <= start_column:
                raise ValueError("結束列必須大於起始列，且兩者必須是非負數。")

            # 獲取輸出文件路徑
            output_folder = input("輸入輸出文件資料夾的路徑: ").strip()
            return folder_path, start_row, end_row, start_column, end_column, output_folder
        except ValueError as e:
            print(f"無效的輸入: {e}. 請再試一次。")


def main():
    # 獲取用戶輸入
    folder_path, start_row, end_row, start_column, end_column, output_folder = get_user_input()

    
    try:
        # 獲取文件夾中的所有文件
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                print(f"處理文件: {file_path}")
                all_values = []
                # 讀取文件中的數據
                values = read_data_range(file_path, start_row, end_row, start_column, end_column)
                all_values.extend(values)
                # 為輸出文件生成唯一的名稱
                base_name = os.path.splitext(file_name)[0]  # 去掉文件擴展名
                output_path = os.path.join(output_folder, f"{base_name}_output.txt")

                save_values_to_txt(all_values, output_path, end_column, start_column)          
    except Exception as e:
        print(f"讀取與儲存數據時出錯: {e}")
        return


    try:
        # 計算輸出文件中的換行符數量
        newline_count = count_newlines(output_path)
        print(f"輸出文件中的換行符數量: {newline_count}")
    except Exception as e:
        print(f"計算換行符時出錯: {e}")


if __name__ == "__main__":
    main()
