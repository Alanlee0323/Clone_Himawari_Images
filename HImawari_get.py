import os
import struct
import subprocess
import sys
from datetime import datetime, timedelta
import shutil
import numpy as np

def is_valid_time_format(time_str):
    if len(time_str) != 12:
        return False
    try:
        int(time_str)
        return True
    except ValueError:
        return False

def generate_urls(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, '%Y%m%d%H%M')
    end_time = datetime.strptime(end_time_str, '%Y%m%d%H%M')
    
    current_time = start_time
    urls = []
    
    while current_time <= end_time:
        url = f"ftp://hmwr829gr.cr.chiba-u.ac.jp/gridded/FD/V20190123/{current_time.strftime('%Y%m')}/EXT/{current_time.strftime('%Y%m%d%H%M')}.ext.01.fld.geoss.bz2"
        urls.append(url)
        current_time += timedelta(minutes=10)
    
    return urls

def write_to_file(urls, start_time_str, end_time_str):
    file_name = f"{start_time_str}-{end_time_str}.txt"
    with open(file_name, 'w') as file:
        for url in urls:
            file.write(url + '\n')


def convert_count_to_tbb(input_filename, convert_table_filename, output_filename):
    NX = 24000
    NY = 12000
    
    # 分配內存
    data_all = np.zeros((NY, NX), dtype=np.uint16)
    dt = np.zeros((NY, NX), dtype=np.float32)
    tbb = np.zeros(5000, dtype=np.float32)
    
    # 讀取數據文件
    try:
        with open(input_filename, 'rb') as f:
            data_all = np.fromfile(f, dtype=np.uint16).reshape((NY*2, NX))
    except FileNotFoundError:
        print(f"*** inputfile ({input_filename}) cannot open ***")
        return
    
    # 讀取 TBB 轉換表
    try:
        with open(convert_table_filename, 'r') as f:
            lines = f.readlines()
            if len(lines) < 5000:
                print(f"*** convert file ({convert_table_filename}) has fewer than 5000 lines ***")
                print(f"Only {len(lines)} lines found. Filling the rest with zero.")
            for i, line in enumerate(lines):
                values = line.strip().split()
                if len(values) != 2:
                    print(f"*** invalid format in convert file ({convert_table_filename}) at line {i+1} ***")
                    return
                tmp_cn, tmp_tbb = map(float, values)
                tbb[int(tmp_cn)] = tmp_tbb
            # 填充剩餘部分
            for j in range(len(lines), 5000):
                tbb[j] = 0.0
    except FileNotFoundError:
        print(f"*** convert file ({convert_table_filename}) cannot open ***")
        return
    
    # 轉換 CNT 到 TBB
    for i in range(NY):
        for j in range(NX):
            cn = data_all[i, j]
            dt[i, j] = tbb[cn]
    
    # 輸出數據
    with open(output_filename, 'wb') as f:
        dt.tofile(f)
    
    print(f"Conversion complete. Output written to {output_filename}")

def process_time_range(start_time_str, end_time_str):
    urls = generate_urls(start_time_str, end_time_str)
    write_to_file(urls, start_time_str, end_time_str)
    print(f"URLs 已生成並寫入至 '{start_time_str}-{end_time_str}.txt' 檔案中。")

    directory_name = f"{start_time_str}_{end_time_str}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    print(f"創建資料夾 '{directory_name}' 來儲存下載的文件。")
    
    try:
        subprocess.run(["wget", "-i", f"{start_time_str}-{end_time_str}.txt", "-P", directory_name], check=True)
        print("文件下載成功。")
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 執行 wget 時發生錯誤，錯誤代碼 {e.returncode}")

    try:
        bz2_files = [f for f in os.listdir(directory_name) if f.endswith('.bz2')]
        for bz2_file in bz2_files:
            subprocess.run(["bunzip2", os.path.join(directory_name, bz2_file)], check=True)
            print(f"'{bz2_file}' 解壓縮完成。")
        print("所有文件解壓縮完成。")
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 執行 bunzip2 時發生錯誤，錯誤代碼 {e.returncode}")

    '''dd Transform to little-endian and delete original files'''
    try:
        geoss_files = [f for f in os.listdir(directory_name) if f.endswith('.geoss')]
        for geoss_file in geoss_files:
            input_file = os.path.join(directory_name, geoss_file)
            output_file = os.path.join(directory_name, "little-endian-" + geoss_file)
            subprocess.run(["dd", f"if={input_file}", f"of={output_file}", "conv=swab"], check=True)
            print(f"'{geoss_file}' 轉換為小端格式完成，輸出檔案為 '{output_file}'。")
        print("所有 .geoss 文件轉換完成。")
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 執行 dd 轉換時發生錯誤，錯誤代碼 {e.returncode}")
    try:
        for geoss_file in geoss_files:
            if not geoss_file.startswith("little-endian"):
                file_to_delete = os.path.join(directory_name, geoss_file)
                os.remove(file_to_delete)
                print(f"已刪除檔案 '{file_to_delete}'。")
        print("非 'little-endian' 檔案刪除完成。")
    except OSError as e:
        print(f"錯誤: 嘗試刪除檔案時發生錯誤，錯誤訊息 {e.strerror}")


    '''tbb Transform'''
    try:
        little_endian_files = [f for f in os.listdir(directory_name) if f.startswith("little-endian")]
        for little_endian_file in little_endian_files:
            input_file_path = os.path.join(directory_name, little_endian_file)
            output_filename = os.path.join(directory_name, "tbb" + little_endian_file)
            convert_count_to_tbb(input_file_path, r'ext.01', output_filename)
            print(f"'{little_endian_file}' 轉換為小端格式完成，輸出檔案為 '{output_filename}'。")
    except OSError as e:
        print(f"錯誤: 嘗試 tbb Transform 時發生錯誤，錯誤訊息 {e.strerror}")
    try:
        for little_endian_file in little_endian_files:
            if not little_endian_file.startswith("tbb"):
                file_to_delete = os.path.join(directory_name, little_endian_file)
                os.remove(file_to_delete)
                print(f"已刪除檔案 '{file_to_delete}'。")
        print("非 'tbb' 檔案刪除完成。")
    except OSError as e:
        print(f"錯誤: 嘗試刪除檔案時發生錯誤，錯誤訊息 {e.strerror}")


    '''只擷取我需要的經緯度'''
    def process_data(folder_path, start_row, end_row, start_column, end_column, output_folder):
        def read_data_range(file_path):
            with open(file_path, 'rb') as file:
                values = []
                for row in range(start_row, end_row):
                    row_start_byte = (row * 24000 + start_column) * 4
                    row_end_byte = (row * 24000 + end_column) * 4
                    file.seek(row_start_byte)
                    row_data = file.read(row_end_byte - row_start_byte)
                    expected_length = (end_column - start_column) * 4
                    if len(row_data) != expected_length:
                        raise ValueError(f"預期 {expected_length} 字節，但獲得 {len(row_data)} 字節")
                    row_values = struct.unpack('f' * (end_column - start_column), row_data)
                    values.extend(row_values)
                return values

        def save_values_to_txt(values, file_path):
            with open(file_path, 'w') as file:
                for i in range(0, len(values), (end_column - start_column)):
                    line = ' '.join(str(value) for value in values[i:i + (end_column - start_column)])
                    file.write(line + '\n')

        def count_newlines(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                return content.count('\n')

        try:
            file_list = os.listdir(folder_path)
            for file_name in file_list:
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    print(f"處理文件: {file_path}")
                    values = read_data_range(file_path)
                    base_name = os.path.splitext(file_name)[0]
                    output_path = os.path.join(output_folder, f"{base_name}_output.txt")
                    save_values_to_txt(values, output_path)

            newline_count = count_newlines(output_path)
            print(f"輸出文件中的換行符數量: {newline_count}")
        except Exception as e:
            print(f"處理數據時出錯: {e}")

        try:
            tbb_files = [f for f in os.listdir(directory_name) if f.startswith('tbb')]
            for tbb_file in tbb_files:
                if not tbb_file.endswith(".txt"):
                    file_to_delete = os.path.join(directory_name, tbb_file)
                    os.remove(file_to_delete)
                    print(f"已刪除檔案 '{file_to_delete}'。")
        except OSError as e:
            print(f"錯誤: 嘗試刪除tbb_file時發生錯誤，錯誤訊息 {e.strerror}")

    folder_path = directory_name
    output_folder = directory_name
    start_row = 7800
    end_row = 8000
    start_column = 6800
    end_column = 7000
    
    process_data(folder_path, start_row, end_row, start_column, end_column, output_folder)

'''主運作邏輯'''
def main():
    # 從用戶那裡讀取包含多個時間區間的文本檔案
    time_ranges_file = r"Download_time_1_6.txt"
    
    try:
        with open(time_ranges_file, 'r') as file:
            time_ranges = file.readlines()
    except IOError:
        print(f"無法打開文件 '{time_ranges_file}'")
        return

    for line in time_ranges:
        start_time_str, end_time_str = line.strip().split()
        start_time_str += "0850"
        end_time_str += "0900"
        
        if not is_valid_time_format(start_time_str) or not is_valid_time_format(end_time_str):
            print(f"時間格式錯誤，請確保格式為 YYYYMMDDHHMM。({line.strip()})")
            continue  # 跳過這個時間區間

        process_time_range(start_time_str, end_time_str)

if __name__ == "__main__":
    main()
