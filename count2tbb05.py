import os 
import numpy as np

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

directory_name = '201906020850_201906020900'
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
