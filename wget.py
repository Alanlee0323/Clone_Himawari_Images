import os
import subprocess
import sys

# 引入 datetime 模組
from datetime import datetime, timedelta

def is_valid_time_format(time_str):
    # 檢查時間格式是否為 YYYYMMDDHHMM
    if len(time_str) != 12:
        return False
    try:
        int(time_str)  # 嘗試將時間字串轉為整數，檢查是否只包含數字
        return True
    except ValueError:
        return False


def generate_urls(start_time_str, end_time_str):
    # 將字串時間轉為 datetime 對象
    start_time = datetime.strptime(start_time_str, '%Y%m%d%H%M')
    end_time = datetime.strptime(end_time_str, '%Y%m%d%H%M')
    
    current_time = start_time
    urls = []
    
    while current_time <= end_time:
        # 格式化URL
        url = f"ftp://hmwr829gr.cr.chiba-u.ac.jp/gridded/FD/V20190123/{current_time.strftime('%Y%m')}/EXT/{current_time.strftime('%Y%m%d%H%M')}.ext.01.fld.geoss.bz2"
        urls.append(url)
        
        # 每次增加10分鐘
        current_time += timedelta(minutes=10)
    
    return urls

def write_to_file(urls, start_time_str, end_time_str):
    file_name = f"{start_time_str}-{end_time_str}.txt"
    with open(file_name, 'w') as file:
        for url in urls:
            file.write(url + '\n')

def convert_file():
    NX = 24000
    NY = 12000
    data_all = []
    dt = []

    # Get input filename from user
    input_filename = input("Enter input filename: ")

    # Open and read data file
    try:
        with open(input_filename, 'rb') as fp:
            data_all = list(fp.read(NX * NY * 2))  # Assuming data is stored as unsigned short (2 bytes)
    except IOError:
        print(f"*** inputfile ({input_filename}) cannot open ***")
        sys.exit(1)

    # Get convert table filename from user
    convert_filename = input("Enter convert table filename: ")

    # Open and read TBB table
    try:
        with open(convert_filename, 'r') as fp:
            tbb = [tuple(map(float, line.split())) for line in fp.readlines()]
    except IOError:
        print(f"*** convert file ({convert_filename}) cannot open ***")
        sys.exit(1)

    # Convert CNT to TBB
    for i in range(NY):
        for j in range(NX):
            cn = data_all[NX * i + j]
            dt.append(tbb[int(cn)][1])

    # Output data
    output_filename = f"grid05_{input_filename}.dat"
    try:
        with open(output_filename, 'wb') as fp:
            fp.write(bytearray(dt))
    except IOError:
        print(f"*** Cannot write to outputfile ({output_filename}) ***")
        sys.exit(1)

    print(f"*** Output file ({output_filename}) created successfully ***")


def main():
    start_time_str = input("請輸入起始時間 (格式如 201907070000): ")
    end_time_str = input("請輸入結束時間 (格式如 201907080000): ")

    # 檢查時間格式
    if not is_valid_time_format(start_time_str) or not is_valid_time_format(end_time_str):
        print("時間格式錯誤，請確保格式為 YYYYMMDDHHMM。")
        return  # 結束程式

    urls = generate_urls(start_time_str, end_time_str)
    write_to_file(urls, start_time_str, end_time_str)
    print(f"URLs 已生成並寫入至 '{start_time_str}-{end_time_str}.txt' 檔案中。")

    # 創建資料夾
    directory_name = f"{start_time_str}_{end_time_str}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    print(f"創建資料夾 '{directory_name}' 來儲存下載的文件。")
    
    # 執行 wget 下載到指定資料夾
    try:
        subprocess.run(["wget", "-i", f"{start_time_str}-{end_time_str}.txt", "-P", directory_name], check=True)
        print("文件下載成功。")
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 執行 wget 時發生錯誤，錯誤代碼 {e.returncode}")

    # 解壓縮資料夾中的所有 .bz2 文件
    try:
        bz2_files = [f for f in os.listdir(directory_name) if f.endswith('.bz2')]
        for bz2_file in bz2_files:
            subprocess.run(["bunzip2", os.path.join(directory_name, bz2_file)], check=True)
            print(f"'{bz2_file}' 解壓縮完成。")
        print("所有文件解壓縮完成。")
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 執行 bunzip2 時發生錯誤，錯誤代碼 {e.returncode}")


        # 對資料夾中的所有 .geoss 文件執行 dd 轉換
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

    # 刪除所有不是以 "little-endian" 開頭的 .geoss 檔案
    try:
        for geoss_file in geoss_files:
            if not geoss_file.startswith("little-endian"):
                file_to_delete = os.path.join(directory_name, geoss_file)
                os.remove(file_to_delete)
                print(f"已刪除檔案 '{file_to_delete}'。")
        print("非 'little-endian' 檔案刪除完成。")
    except OSError as e:
        print(f"錯誤: 嘗試刪除檔案時發生錯誤，錯誤訊息 {e.strerror}")


# 確認這個檔案被執行，而不是被引入
if __name__ == "__main__":
    main()
