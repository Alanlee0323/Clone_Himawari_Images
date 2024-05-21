import sys
import os

def convert_file(input_filename, convert_filename):
    NX = 24000
    NY = 12000
    data_all = []
    dt = []

    # Open and read data file
    try:
        with open(input_filename, 'rb') as fp:
            data_all = list(fp.read(NX * NY * 2))  # Assuming data is stored as unsigned short (2 bytes)
    except IOError:
        print(f"*** inputfile ({input_filename}) cannot open ***")
        sys.exit(1)

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
            dt.append(int(tbb[cn][1]))

    # Output data
    output_filename = f"{input_filename}.dat"
    try:
        with open(output_filename, 'wb') as fp:
            fp.write(bytearray(dt))
    except IOError:
        print(f"*** Cannot write to outputfile ({output_filename}) ***")
        sys.exit(1)

    print(f"*** Output file ({output_filename}) created successfully ***")

def main():
    # 使用者輸入目錄路徑
    directory_path = input("Please enter the directory path: ")
    
    # 檢查目錄是否存在
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        sys.exit(1)

    # 獲取目錄中所有 .geoss 檔案的路徑
    geoss_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.geoss')]

    # 使用者輸入轉換檔案的路徑
    convert_filename = input("Please enter the conversion file path: ")

    # 對每個 .geoss 檔案執行轉換
    for geoss_file in geoss_files:
        convert_file(geoss_file, convert_filename)

if __name__ == "__main__":
    main()
